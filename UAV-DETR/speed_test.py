"""
UAV-DETR speed benchmark on real VisDrone images.

Usage:
    python speed_test.py --weights uavdetr_r50/exp2/weights/best.pt --data ../VisDrone.yaml
    python speed_test.py --model uavdetr-r50.yaml --data ../VisDrone.yaml --device cpu
"""

import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch
import yaml
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

from ultralytics import RTDETR
from ultralytics.nn.tasks import attempt_load_weights
from ultralytics.utils.torch_utils import select_device


IMAGENET_DEFAULT_MEAN = [0.485, 0.456, 0.406]
IMAGENET_DEFAULT_STD  = [0.229, 0.224, 0.225]


def load_image_paths(data_yaml: str, split: str = "test", max_images: int = 500) -> list:
    """Read image paths from the data yaml config."""
    with open(data_yaml) as f:
        cfg = yaml.safe_load(f)

    img_dir = cfg.get(split, None)
    if img_dir is None or not os.path.isdir(img_dir):
        raise FileNotFoundError(f"Image directory not found for split '{split}': {img_dir}")

    exts = {'.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff'}
    paths = sorted([
        os.path.join(img_dir, p) for p in os.listdir(img_dir)
        if os.path.splitext(p)[1].lower() in exts
    ])
    if not paths:
        raise RuntimeError(f"No images found in {img_dir}")

    print(f"Found {len(paths)} images in {img_dir}, using {min(len(paths), max_images)}")
    return paths[:max_images]


def get_transform(imgsz: int):
    """ImageNet-style normalization used by RT-DETR."""
    return transforms.Compose([
        transforms.Resize((imgsz, imgsz)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_DEFAULT_MEAN, std=IMAGENET_DEFAULT_STD),
    ])


def load_images(paths: list, imgsz: int, device: torch.device) -> torch.Tensor:
    """Preload all images into a single tensor on device (may use lots of GPU RAM)."""
    transform = get_transform(imgsz)
    tensors = []
    for p in tqdm(paths, desc="Loading images", leave=False):
        img = Image.open(p).convert("RGB")
        tensors.append(transform(img))
    return torch.stack(tensors).to(device).float()


@torch.no_grad()
def run_benchmark(model, images: torch.Tensor, batch: int,
                  warmup: int, rounds: int, device: torch.device):
    """Latency / throughput benchmark with real images."""
    n_images = images.shape[0]
    # pre-generate batches
    batches = []
    for start in range(0, n_images, batch):
        batch_imgs = images[start: start + batch]
        # pad to fixed batch size
        if batch_imgs.shape[0] < batch:
            pad = batch - batch_imgs.shape[0]
            batch_imgs = torch.cat([batch_imgs, images[:pad]], dim=0)
        batches.append(batch_imgs.to(device))

    # --- warmup ---
    print(f"Warming up ({warmup} iters) ...")
    for _ in tqdm(range(warmup), desc="Warmup", leave=False):
        model(batches[0])

    # --- measure ---
    print(f"Benchmarking ({rounds} rounds) ...")
    if device.type == "cuda":
        start_ev = [torch.cuda.Event(enable_timing=True) for _ in range(rounds)]
        end_ev   = [torch.cuda.Event(enable_timing=True) for _ in range(rounds)]

    latencies = []
    for i in tqdm(range(rounds), desc="Benchmark"):
        batch_imgs = batches[i % len(batches)]
        if device.type == "cuda":
            start_ev[i].record()
            model(batch_imgs)
            end_ev[i].record()
        else:
            t0 = time.perf_counter()
            model(batch_imgs)
            t1 = time.perf_counter()
            latencies.append((t1 - t0) / batch * 1000)

    if device.type == "cuda":
        torch.cuda.synchronize()
        latencies = [(s.elapsed_time(e)) / batch for s, e in zip(start_ev, end_ev)]

    latencies = np.array(latencies)
    per_image_ms = np.mean(latencies)
    fps = 1000.0 / per_image_ms
    return {
        "batch_size": batch,
        "imgsz": images.shape[-1],
        "warmup": warmup,
        "rounds": rounds,
        "latency_ms": round(per_image_ms, 2),
        "latency_std_ms": round(np.std(latencies), 2),
        "fps": round(fps, 2),
        "device": str(device),
    }


def main():
    parser = argparse.ArgumentParser(description="UAV-DETR Speed Benchmark")
    parser.add_argument("--weights", type=str, default=None,
                        help="Path to .pt checkpoint")
    parser.add_argument("--model", type=str, default=None,
                        help="Path to model .yaml (e.g. ultralytics/cfg/models/uavdetr-r50.yaml)")
    parser.add_argument("--data", type=str, default="../VisDrone.yaml",
                        help="Dataset yaml for real image paths")
    parser.add_argument("--split", type=str, default="test",
                        help="Dataset split: train / val / test")
    parser.add_argument("--imgsz", type=int, default=640, help="Input image size")
    parser.add_argument("--batch", type=int, default=1, help="Batch size")
    parser.add_argument("--warmup", type=int, default=50, help="Warmup iterations")
    parser.add_argument("--rounds", type=int, default=500, help="Benchmark iterations")
    parser.add_argument("--max-images", type=int, default=200,
                        help="Max real images to load (keeps RAM manageable)")
    parser.add_argument("--device", type=str, default="0", help="Device (0, cpu, etc.)")
    parser.add_argument("--fp16", action="store_true", help="Use FP16")
    parser.add_argument("--fuse", action="store_true", help="Fuse Conv+BN layers")
    args = parser.parse_args()

    if args.weights is None and args.model is None:
        parser.error("Must provide --weights or --model")

    device = select_device(args.device, batch=args.batch)
    print(f"Device: {device}")

    # --- Load model ---
    if args.weights and args.weights.endswith(".pt"):
        print(f"Loading checkpoint: {args.weights}")
        model = attempt_load_weights(args.weights, device=device)
    elif args.model:
        print(f"Loading from yaml: {args.model}")
        model = RTDETR(args.model).model
    else:
        raise ValueError("Unsupported weights/model format")

    model = model.to(device).float()
    model.eval()
    if args.fuse:
        model.fuse()
        print("Model fused.")
    if args.fp16:
        model = model.half()

    # --- Load images ---
    img_paths = load_image_paths(args.data, args.split, max_images=args.max_images)
    images = load_images(img_paths, args.imgsz, device)
    if args.fp16:
        images = images.half()

    # --- Benchmark ---
    result = run_benchmark(model, images, args.batch, args.warmup, args.rounds, device)

    # --- Report ---
    print("\n" + "=" * 52)
    print("  UAV-DETR Speed Benchmark")
    print("=" * 52)
    print(f"  Model:       {args.weights or args.model}")
    print(f"  Device:      {result['device']}")
    print(f"  Precision:   {'FP16' if args.fp16 else 'FP32'}")
    print(f"  Image size:  {result['imgsz']}x{result['imgsz']}")
    print(f"  Batch size:  {result['batch_size']}")
    print(f"  Warmup:      {result['warmup']} iters")
    print(f"  Rounds:      {result['rounds']} iters")
    print(f"  Real images: {len(img_paths)}")
    print("-" * 52)
    print(f"  Latency:     {result['latency_ms']} ms  (±{result['latency_std_ms']} ms)")
    print(f"  FPS:         {result['fps']}")
    print("=" * 52)


if __name__ == "__main__":
    main()
