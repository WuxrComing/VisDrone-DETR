import warnings
import os
from pathlib import Path
from ultralytics import RTDETR
import torch

os.environ['WANDB_MODE'] = 'disabled'
warnings.filterwarnings('ignore')


def check_path(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")


if __name__ == '__main__':
    torch.cuda.empty_cache()

    current_dir = Path(__file__).parent
    yaml_path = '../VisDrone.yaml'
    check_path(yaml_path)

    # Path to the checkpoint to resume from
    resume_ckpt = './uavdetr_r50/exp2/weights/last.pt'
    check_path(resume_ckpt)

    model = RTDETR('./ultralytics/cfg/models/uavdetr-r50.yaml')
    model.train(data=str(yaml_path),
                cache=False,
                imgsz=800,
                epochs=400,
                batch=2,
                workers=4,
                device='0',
                resume=resume_ckpt,
                project='uavdetr_r50',
                name='exp2',
                patience=40,
                exist_ok=True,  # continue writing to the same exp2 directory
                )
