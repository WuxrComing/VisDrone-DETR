#!/usr/bin/env python3
"""
VisDrone 预训练权重模型对比评估 (weight/ 目录下 S/M/L)

对比 Dome-S / Dome-M / Dome-L 在验证集和测试集上的精度与速度。

用法:
    python eval_weight_models.py                          # 评估全部模型 val+test
    python eval_weight_models.py --model dome_s dome_m    # 只评估指定模型
    python eval_weight_models.py --split val              # 只评估验证集
    python eval_weight_models.py --bench                  # 纯推理速度基准测试
    python eval_weight_models.py --bench --model dome_m   # 指定模型 benchmark
"""

import argparse
import os
import re
import subprocess
import sys
import threading
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# 模型: 权重位于 weight/ 目录, 对应各自的配置文件
# ---------------------------------------------------------------------------
MODELS = {
    "dome_s": {
        "ckpt": "weight/dome-s-visdrone_converted.pth",
        "config": "configs/dome/Dome-S-VisDrone.yml",
        "desc": "Dome-S (HGNetv2-B0)",
    },
    "dome_m": {
        "ckpt": "weight/dome-m-visdrone_converted.pth",
        "config": "configs/dome/Dome-M-VisDrone.yml",
        "desc": "Dome-M (HGNetv2-B2)",
    },
    "dome_l": {
        "ckpt": "weight/dome-l-visdrone_converted.pth",
        "config": "configs/dome/Dome-L-VisDrone.yml",
        "desc": "Dome-L (HGNetv2-B4)",
    },
}

# ---------------------------------------------------------------------------
# 数据集路径
# ---------------------------------------------------------------------------
DATASETS = {
    "val": {
        "img": "/mnt/nas/DataSet/VisDrone/VisDrone2019-DET-val/images",
        "ann": "/mnt/nas/DataSet/VisDrone/annotations_coco/VisDrone2019-DET_val_coco.json",
        "desc": "验证集 (548图, 10类)",
        "num_images": 548,
    },
    "test": {
        "img": "/mnt/nas/DataSet/VisDrone/VisDrone2019-DET-test-dev/images",
        "ann": "/mnt/nas/DataSet/VisDrone/annotations_coco/VisDrone2019-DET_test_coco.json",
        "desc": "测试集 (1609图, 10类)",
        "num_images": 1609,
    },
}

# 从 COCO eval 输出中提取的指标
METRIC_PATTERNS = [
    (r'AP\).*IoU=0\.50:0\.95.*area=\s*all.*=\s*([-\d\.]+)', "AP"),
    (r'AP\).*IoU=0\.50[^:].*area=\s*all.*=\s*([-\d\.]+)', "AP_50"),
    (r'AP\).*IoU=0\.75.*area=\s*all.*=\s*([-\d\.]+)', "AP_75"),
    (r'AP\).*IoU=0\.50:0\.95.*area=\s*small\b.*=\s*([-\d\.]+)', "AP_small"),
    (r'AP\).*IoU=0\.50:0\.95.*area=medium.*=\s*([-\d\.]+)', "AP_medium"),
    (r'AP\).*IoU=0\.50:0\.95.*area=\s*large\b.*=\s*([-\d\.]+)', "AP_large"),
    (r'AR\).*IoU=0\.50:0\.95.*area=\s*all.*maxDets=\s*1[^\d].*=\s*([-\d\.]+)', "AR@1"),
    (r'AR\).*IoU=0\.50:0\.95.*area=\s*all.*maxDets=\s*10[^\d].*=\s*([-\d\.]+)', "AR@10"),
    (r'AR\).*IoU=0\.50:0\.95.*area=\s*all.*maxDets=100.*=\s*([-\d\.]+)', "AR@100"),
    (r'Total time:\s*(\d+):(\d+):(\d+)', "TOTAL_TIME"),
]

METRIC_DISPLAY_ORDER = [
    "AP", "AP_50", "AP_75",
    "AP_small", "AP_medium", "AP_large",
    "AR@1", "AR@10", "AR@100",
    "FPS", "Latency",
]


def stream_reader(pipe, buf: list[str]):
    for line in iter(pipe.readline, ""):
        sys.stdout.write(line)
        sys.stdout.flush()
        buf.append(line)
    pipe.close()


def run_eval(model_key: str, split: str) -> dict[str, float]:
    """运行 test-only 评估, 返回提取的指标。"""
    ckpt = PROJECT_DIR / MODELS[model_key]["ckpt"]
    config = MODELS[model_key]["config"]
    if not ckpt.exists():
        print(f"\n  [ERROR] Checkpoint 不存在: {ckpt}\n")
        sys.exit(1)

    ds = DATASETS[split]

    cmd = [
        sys.executable, str(PROJECT_DIR / "train.py"),
        "-c", config,
        "-r", str(ckpt),
        "--test-only",
        "--update",
        f"val_dataloader.dataset.img_folder={ds['img']}",
        f"val_dataloader.dataset.ann_file={ds['ann']}",
    ]

    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "0"

    p = subprocess.Popen(
        cmd, cwd=str(PROJECT_DIR),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, env=env,
    )

    lines: list[str] = []
    t = threading.Thread(target=stream_reader, args=(p.stdout, lines))
    t.daemon = True
    t.start()

    p.wait()
    t.join(timeout=10)

    output = "".join(lines)
    metrics = {}

    for pattern, name in METRIC_PATTERNS:
        m = re.search(pattern, output)
        if m:
            if name == "TOTAL_TIME":
                h, mm, ss = int(m.group(1)), int(m.group(2)), int(m.group(3))
                total_sec = h * 3600 + mm * 60 + ss
                num_imgs = DATASETS[split].get("num_images", 0)
                if total_sec > 0 and num_imgs > 0:
                    metrics["Latency"] = total_sec * 1000 / num_imgs
                    metrics["FPS"] = num_imgs / total_sec
            else:
                val = float(m.group(1))
                if val != -1.000:
                    metrics[name] = val

    return metrics


def print_table(rows: list[dict], col_keys: list[str], col_widths: list[int]):
    top = "  ┌" + "┬".join("─" * w for w in col_widths) + "┐"
    sep = "  ├" + "┼".join("─" * w for w in col_widths) + "┤"
    bot = "  └" + "┴".join("─" * w for w in col_widths) + "┘"

    print(top)
    for i, row in enumerate(rows):
        cells = [str(row.get(k, "-")).ljust(w) for k, w in zip(col_keys, col_widths)]
        print("  │" + "│".join(cells) + "│")
        if i == 0 and len(rows) > 1:
            print(sep)
    print(bot)


def run_bench(model_key: str, warmup: int, repeat: int) -> dict[str, float]:
    """单图重复推理, 测量纯推理 latency / FPS。"""
    import torch
    import torch.nn as nn
    import torchvision.transforms as T
    from PIL import Image

    sys.path.insert(0, str(PROJECT_DIR))
    from src.core import YAMLConfig

    config = MODELS[model_key]["config"]
    ckpt_path = PROJECT_DIR / MODELS[model_key]["ckpt"]

    print(f"\n  ▶ [{model_key}] Bench (warmup={warmup}, repeat={repeat})")
    sys.stdout.flush()

    if not ckpt_path.exists():
        print(f"\n  [ERROR] Checkpoint 不存在: {ckpt_path}\n")
        sys.exit(1)

    # 加载模型
    cfg = YAMLConfig(str(PROJECT_DIR / config), resume=str(ckpt_path))
    if "HGNetv2" in cfg.yaml_cfg:
        cfg.yaml_cfg["HGNetv2"]["pretrained"] = False

    checkpoint = torch.load(str(ckpt_path), map_location="cpu")
    if "ema" in checkpoint:
        state = checkpoint["ema"]["module"]
    else:
        state = checkpoint.get("model", checkpoint)
    cfg.model.load_state_dict(state, strict=False)

    class DeployModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.model = cfg.model.deploy()
            self.postprocessor = cfg.postprocessor.deploy()

        def forward(self, images, orig_target_sizes):
            outputs = self.model(images)
            return self.postprocessor(outputs, orig_target_sizes)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DeployModel().to(device)
    model.eval()

    # 加载一张图片
    val_img_dir = DATASETS["val"]["img"]
    img_files = sorted(os.listdir(val_img_dir))
    img_path = os.path.join(val_img_dir, img_files[0])
    print(f"  图像: {img_path}")

    im_pil = Image.open(img_path).convert("RGB")
    w, h = im_pil.size
    orig_size = torch.tensor([[w, h]]).to(device)

    transforms = T.Compose([T.Resize((800, 800)), T.ToTensor()])
    im_data = transforms(im_pil).unsqueeze(0).to(device)

    # Warmup
    print(f"  Warming up ({warmup} iters)...")
    with torch.no_grad():
        for _ in range(warmup):
            _ = model(im_data, orig_size)
    if device.type == "cuda":
        torch.cuda.synchronize()

    # Benchmark
    print(f"  Benchmarking ({repeat} iters)...")
    if device.type == "cuda":
        starter = torch.cuda.Event(enable_timing=True)
        ender = torch.cuda.Event(enable_timing=True)
        starter.record()
        with torch.no_grad():
            for _ in range(repeat):
                _ = model(im_data, orig_size)
        ender.record()
        torch.cuda.synchronize()
        elapsed_ms = starter.elapsed_time(ender)
    else:
        import time
        t0 = time.perf_counter()
        with torch.no_grad():
            for _ in range(repeat):
                _ = model(im_data, orig_size)
        elapsed_ms = (time.perf_counter() - t0) * 1000

    latency = elapsed_ms / repeat
    fps = 1000.0 / latency

    print(f"  Latency: {latency:.2f} ms  |  FPS: {fps:.2f}")
    return {"Latency": latency, "FPS": fps}


def main():
    parser = argparse.ArgumentParser(description="VisDrone 预训练权重模型评估")
    parser.add_argument("--model", nargs="+", choices=list(MODELS.keys()),
                        help="指定模型 (默认全部 S/M/L)")
    parser.add_argument("--split", nargs="+", choices=["val", "test"],
                        help="指定数据集 (默认全部)")
    parser.add_argument("--bench", action="store_true",
                        help="纯推理速度基准测试 (单图重复)")
    parser.add_argument("--warmup", type=int, default=50,
                        help="Bench 预热迭代次数 (默认 50)")
    parser.add_argument("--repeat", type=int, default=200,
                        help="Bench 测试迭代次数 (默认 200)")
    args = parser.parse_args()

    models = args.model or list(MODELS.keys())

    # ---- Bench 模式 ----
    if args.bench:
        print()
        print("=" * 70)
        print("  VisDrone 推理速度基准测试 (纯推理, 单图重复)")
        bench_desc = ", ".join(MODELS[m]["desc"] for m in models)
        print(f"  模型:    {bench_desc}")
        print(f"  Warmup:  {args.warmup}  |  Repeat:  {args.repeat}")
        print("=" * 70)
        sys.stdout.flush()

        all_bench = {}
        for model_key in models:
            all_bench[model_key] = run_bench(model_key, args.warmup, args.repeat)

        print()
        col_keys = ["指标", "Latency", "FPS"]
        col_widths = [24, 12, 10]
        rows = []
        for model_key in models:
            m = all_bench[model_key]
            rows.append({"指标": MODELS[model_key]["desc"],
                         "Latency": f"{m['Latency']:.2f}",
                         "FPS": f"{m['FPS']:.2f}"})
        print_table(rows, col_keys, col_widths)

        if len(models) >= 2:
            print()
            print(f"  {'=' * 68}")
            print(f"  模型间差异")
            print(f"  {'=' * 68}")
            for i in range(len(models)):
                for j in range(i + 1, len(models)):
                    mi, mj = models[i], models[j]
                    ri, rj = all_bench[mi], all_bench[mj]
                    print(f"\n  Δ = {MODELS[mj]['desc']} - {MODELS[mi]['desc']}")
                    for k in ["Latency", "FPS"]:
                        d = rj[k] - ri[k]
                        s = "+" if d >= 0 else ""
                        print(f"    {k:<10s}: {s}{d:+.2f}")
        print()
        return

    # ---- 正常评估模式 ----
    splits = args.split or list(DATASETS.keys())

    print()
    print("=" * 70)
    print("  VisDrone 预训练权重模型评估")
    model_desc = ", ".join(MODELS[m]["desc"] for m in models)
    dataset_desc = ", ".join(DATASETS[s]["desc"] for s in splits)
    print(f"  模型:    {model_desc}")
    print(f"  数据集:  {dataset_desc}")
    print("=" * 70)
    sys.stdout.flush()

    all_results: dict[str, dict[str, dict[str, float]]] = {}

    for split in splits:
        all_results[split] = {}
        for model_key in models:
            print(f"\n  ▶ [{model_key}] 评估 {DATASETS[split]['desc']} ...")
            sys.stdout.flush()
            all_results[split][model_key] = run_eval(model_key, split)

    # ---- 汇总表格 ----
    for split in splits:
        print()
        print(f"  {'=' * 68}")
        print(f"  [{DATASETS[split]['desc']}] 结果对比")
        print(f"  {'=' * 68}")

        rows = []
        for model_key in models:
            m = all_results[split].get(model_key, {})
            row = {"指标": MODELS[model_key]["desc"]}
            for name in METRIC_DISPLAY_ORDER:
                if name in m:
                    row[name] = f"{m[name]:.4f}"
            rows.append(row)

        col_keys = ["指标"] + METRIC_DISPLAY_ORDER
        col_widths = [24] + [10] * len(METRIC_DISPLAY_ORDER)
        print_table(rows, col_keys, col_widths)

    # ---- 模型间差异 ----
    if len(models) >= 2:
        print()
        print(f"  {'=' * 68}")
        print(f"  模型间差异")
        print(f"  {'=' * 68}")

        for split in splits:
            print(f"\n  [{DATASETS[split]['desc']}]")
            for i in range(len(models)):
                for j in range(i + 1, len(models)):
                    mi, mj = models[i], models[j]
                    ri = all_results[split].get(mi, {})
                    rj = all_results[split].get(mj, {})
                    print(f"\n  Δ = {MODELS[mj]['desc']} - {MODELS[mi]['desc']}")
                    for name in METRIC_DISPLAY_ORDER:
                        v1 = ri.get(name)
                        v2 = rj.get(name)
                        if v1 is not None and v2 is not None:
                            d = v2 - v1
                            s = "+" if d >= 0 else ""
                            print(f"    {name:<14s}: {s}{d:+.4f}")

    print()
    print("=" * 70)
    print("  评估完成")
    print("=" * 70)
    print()


if __name__ == "__main__":
    main()
