# DQ-DETR: DETR with Dynamic Query for Tiny Object Detection

![method](./figure/model_final_V4.pdf)

* This repository is an official implementation of the paper DQ-DETR: DETR with Dynamic Query for Tiny Object Detection.
* The original repository link was https://github.com/Katie0723/DQ-DETR. Here is the updated link.


## News
[2024/12/06] We released the organized datasets AI-TOD-V1 and AI-TOD-V2.

[2024/7/1]: **DQ-DETR** has been accepted by **ECCV 2024**. 🔥🔥🔥

[2024/5/3]: **DNTR** has been accepted by **TGRS 2024**. 🔥🔥🔥


## Installation -- Compiling CUDA operators
* The code are built upon the official [DINO DETR](https://github.com/IDEA-Research/DINO) repository.

```sh
conda create -n dqdetr python=3.9 --y
conda activate dqdetr
bash install.sh
```

<!-- # bash scripts/DQ_eval.sh /nfs/home/hoiliu/dqdetr/weights/dqdetr_best305.pth -->
## Eval models
```sh
bash scripts/DQ_eval.sh /path/to/your/dataset /path/to/your/checkpoint
```

## Trained Model
* Changed the pretrained model path in DQ.sh
```sh
CUDA_VISIBLE_DEVICES=5,6,7 bash scripts/DQ.sh /path/to/your/dataset
```

## Our works on Tiny Object Detection 
| Title | Venue | Links | 
|------|-------------|-------|
| **DNTR** | TGRS 2024  | [Paper](https://arxiv.org/abs/2406.05755) \| [code](https://github.com/hoiliu-0801/DNTR) |  \| [中文解读](https://blog.csdn.net/qq_40734883/article/details/142579516) | 
| **DQ-DETR**| ECCV 2024 | [Paper](https://arxiv.org/abs/2404.03507)  \| [code](https://github.com/hoiliu-0801/DQ-DETR) |  \| [中文解读](https://blog.csdn.net/csdn_xmj/article/details/142813757) | 


## Performance
Table 1. **Training Set:** AI-TOD-V2 trainval set, **Testing Set:** AI-TOD-V2 test set, 36 epochs, where FRCN, DR denotes Faster R-CNN and DetectoRS, respectively.
|Method | Backbone | mAP | AP<sub>50</sub> | AP<sub>75</sub> |AP<sub>vt</sub> | AP<sub>t</sub>  | AP<sub>s</sub>  | AP<sub>m</sub> | 
|:---:|:---:|:---:|:---:|:---:|:---:|:---: |:---: |:---: |
Faster R-CNN | R-50 | 11.1 | 26.3 | 7.6 | 0.0 | 7.2 | 23.3 | 33.6 | 
NWD-RKA | R-50 | 23.4 | 53.5 | 16.8 | 8.7 | 23.8 | 28.5 | 36.0 |
DAB-DETR | R-50 | 22.4 | 55.6 | 14.3 | 9.0 | 21.7 | 28.3 | 38.7 | 
DINO-DETR | R-50 | 25.9 | 61.3 | 17.5 | 12.7 | 25.3 | 32.0 | 39.7 | 
DQ-DETR | R-50 | **30.5** | **69.2** | **22.7** | **15.2** | **30.9** | **36.8** | **45.5** | 

## VisDrone Evaluation

DQ-DETR now uses a VisDrone-specific evaluator (`VisdroneCocoEvaluator`) aligned with [Dome-DETR](https://github.com/Katie0723/Dome-DETR). The evaluator is automatically selected when `--dataset_file visdrone`.

### Changes from AI-TOD Evaluator

| Parameter | AI-TOD (CocoEvaluator) | VisDrone (VisdroneCocoEvaluator) |
|-----------|----------------------|----------------------------------|
| maxDets | [1, 100, 1500] | [1, 10, 100, 500] |
| areaRng | all / verytiny (<8²) / tiny (8²~16²) / small (16²~32²) / medium (>32²) | all / small (<32²) / medium (32²~96²) / large (>96²) |
| stats count | 19 (includes LRP-Error ×5) | 13 (no LRP) |
| ignore region filtering | None | IoF > 0.5 |

### maxDets Verification

We verified that changing `maxDets[-1]` from 500 to 1500 has **zero effect** on all metrics (AP, AR, per-area breakdown all identical to 3 decimal places). This is because the model outputs at most `num_select=300` detections per image, well below either threshold.

| Setting | AP_all | AP_50 | AP_75 | AR_100 | AR_maxDets |
|---------|--------|-------|-------|--------|------------|
| maxDets=500 | 0.257 | 0.436 | 0.263 | 0.468 | 0.474 |
| maxDets=1500 | 0.257 | 0.436 | 0.263 | 0.468 | 0.474 |

### Why Results Differ from Old Evaluator

1. **Area ranges are remapped** — new `AP_small` covers all objects < 32² (old verytiny + tiny + small), pulling in harder-to-detect verytiny/tiny objects. New `AP_medium` is capped at 96², excluding large objects. These labels are not comparable to old AI-TOD labels.
2. **Ignore region filtering** — VisDrone annotations contain ignore regions (`category_id=0`, `iscrowd=1`, `ignore=1`). The new evaluator filters out detections with IoF > 0.5 against these regions, reducing false positives.

## AI-TOD-v1 and AI-TOD-v2 Datasets (Don’t forget to leave us a ⭐)
* Step 1: Download the datasets from the below link.
```sh
https://drive.google.com/drive/folders/1CowS5BrujefWQxxlmOFfUuLOfUUm8w6U?usp=sharing
```


* Step 2: Organize the downloaded files in the following way.
```sh
├─ Dataset
│   └─ aitod
│       ├─ annotations
│       ├─ images
│       ├─ test
│       ├─ train
│       ├─ trainval
│       └─ val
├─ DQ-DETR
```

## Pretrained Weights 
* Referred to checkpoint.txt for more details.

* https://reurl.cc/NlvV2Q


## Citation
```bibtex

@InProceedings{huang2024dq,
author={Huang, Yi-Xin and Liu, Hou-I and Shuai, Hong-Han and Cheng, Wen-Huang},
title={DQ-DETR: DETR with Dynamic Query for Tiny Object Detection},
booktitle={European Conference on Computer Vision},
pages={290--305},
year={2025},
organization={Springer}
}

@ARTICLE{10518058,
  author={Liu, Hou-I and Tseng, Yu-Wen and Chang, Kai-Cheng and Wang, Pin-Jyun and Shuai, Hong-Han and Cheng, Wen-Huang},
  journal={IEEE Transactions on Geoscience and Remote Sensing}, 
  title={A DeNoising FPN With Transformer R-CNN for Tiny Object Detection}, 
  year={2024},
  volume={62},
  number={},
  pages={1-15},
}
