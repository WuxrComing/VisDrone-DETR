# VisDrone-DETR

DETR-based tiny object detection on [VisDrone-2019-DET](https://github.com/VisDrone/VisDrone2018-DET-toolkit) — 复现与统一基准。

## 子项目

| Model | Venue | Backbone | 目录 |
|-------|-------|-----------|------|
| **DQ-DETR** — Dynamic Query for Tiny Object Detection | ECCV 2024 | ResNet-50 | [`DQ-DETR/`](DQ-DETR/) |
| **Dome-DETR** — Density-Oriented Feature-Query Manipulation | ACMMM 2025 | HGNetv2-B0/B2/B4 | [`Dome-DETR/`](Dome-DETR/) |
| **UAV-DETR** — Efficient End-to-End Detection for UAV Imagery | arXiv 2025 | ResNet-18/50, EfficientFormerV2 | [`UAV-DETR/`](UAV-DETR/) |

## 评估协议

统一使用 **VisdroneCocoEvaluator**:

- `maxDets = [1, 10, 100, 500]`
- 面积范围: `small (<32²)`, `medium (32²–96²)`, `large (>96²)`
- 忽略区域过滤 (IoF > 0.5)
- 13 个 COCO-style 统计量
- FPS/Latency 在 RTX 4090 上测量

详见 [`docs/evaluation.md`](docs/evaluation.md)。

## 结果

### 验证集 (Val, 548 images, 10 classes)

| Model | Backbone | AP | AP₅₀ | AP₇₅ | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS |
|-------|----------|----:|-----:|-----:|-----:|-----:|-----:|-----:|------:|-------:|----:|
| DQ-DETR | R-50 | 0.323 | 0.520 | 0.333 | 0.244 | 0.412 | 0.531 | 0.132 | 0.384 | 0.526 | 2.5 |
| Dome-Baseline | HGNetv2-B2 | 0.378 | 0.592 | 0.397 | 0.298 | 0.481 | 0.595 | 0.139 | 0.412 | 0.549 | 15.2 |
| Dome-M | HGNetv2-B2 | 0.375 | 0.590 | 0.398 | 0.294 | 0.478 | 0.575 | 0.142 | 0.414 | 0.553 | 15.3 |
| Dome-S (weight) | HGNetv2-B0 | 0.347 | 0.561 | 0.360 | 0.269 | 0.451 | 0.567 | 0.134 | 0.389 | 0.526 | 16.7 |
| Dome-M (weight) | HGNetv2-B2 | 0.382 | 0.607 | 0.401 | 0.302 | 0.489 | 0.623 | 0.142 | 0.417 | 0.556 | 16.1 |
| Dome-L (weight) | HGNetv2-B4 | 0.383 | 0.609 | 0.400 | 0.303 | 0.489 | 0.628 | 0.143 | 0.417 | 0.555 | 15.0 |

### 测试集 (Test, 1609 images, 10 classes)

| Model | Backbone | AP | AP₅₀ | AP₇₅ | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS |
|-------|----------|----:|-----:|-----:|-----:|-----:|-----:|-----:|------:|-------:|----:|
| DQ-DETR | R-50 | 0.257 | 0.436 | 0.263 | 0.163 | 0.342 | 0.463 | 0.102 | 0.331 | 0.468 | 2.7 |
| Dome-Baseline | HGNetv2-B2 | 0.291 | 0.486 | 0.297 | 0.191 | 0.397 | 0.515 | 0.107 | 0.344 | 0.476 | 15.2 |
| Dome-M | HGNetv2-B2 | 0.289 | 0.485 | 0.296 | 0.191 | 0.394 | 0.515 | 0.105 | 0.343 | 0.480 | 15.3 |
| Dome-S (weight) | HGNetv2-B0 | 0.266 | 0.452 | 0.270 | 0.169 | 0.369 | 0.511 | 0.101 | 0.325 | 0.452 | 16.7 |
| Dome-M (weight) | HGNetv2-B2 | 0.291 | 0.489 | 0.297 | 0.190 | 0.401 | 0.528 | 0.108 | 0.347 | 0.479 | 16.1 |
| Dome-L (weight) | HGNetv2-B4 | 0.293 | 0.493 | 0.298 | 0.189 | 0.401 | 0.536 | 0.109 | 0.346 | 0.477 | 15.0 |

### 详细数据

每个模型的原始 COCO 评估输出及评估器对比验证见：

- [`docs/dq-detr.md`](docs/dq-detr.md) — DQ-DETR 完整评估 + 新旧评估器对比
- [`docs/dome-detr.md`](docs/dome-detr.md) — Dome-DETR Baseline / Dome-M / 预训练权重 S/M/L

## 致谢

本项目基于以下工作：

- [**DQ-DETR**](https://github.com/hoiliu-0801/DQ-DETR) — DETR with Dynamic Query for Tiny Object Detection (ECCV 2024)
- [**Dome-DETR**](https://github.com/RicePasteM/Dome-DETR) — Density-Oriented Feature-Query Manipulation for Efficient Tiny Object Detection (ACMMM 2025)
- [**UAV-DETR**](https://github.com/ValiantDiligent/UAV-DETR) — Efficient End-to-End Object Detection for Unmanned Aerial Vehicle Imagery

## License

[Apache 2.0](LICENSE)
