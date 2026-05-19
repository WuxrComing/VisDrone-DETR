# VisDrone 模型总览

> **注意**: DQ-DETR 已升级为 VisDrone 专用评估器（`VisdroneCocoEvaluator`），与 Dome-DETR 对齐。
> 评估参数: `maxDets=[1,10,100,500]`, areaRng: all/small(<32²)/medium(32²~96²)/large(>96²), 13 stats, ignore region 过滤 (IoF>0.5)。

## 验证集 (Val, 548 images)

| Model | Backbone | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **DQ-DETR** | R-50 | 0.359* | 0.589* | 0.366* | — | — | — | 0.136* | — | 0.578* | 6.20 | 161.4 |
| Dome-DETR Baseline | HGNetv2-B2 | 0.378 | 0.592 | 0.397 | 0.298 | 0.481 | 0.595 | 0.139 | 0.412 | 0.549 | 15.2 | 66.0 |
| Dome-DETR Dome-M | HGNetv2-B2 | 0.375 | 0.590 | 0.398 | 0.294 | 0.478 | 0.575 | 0.142 | 0.414 | 0.553 |  15.3 | 65.4 |
| Dome-S (weight) | HGNetv2-B0 | 0.347 | 0.561 | 0.360 | 0.269 | 0.451 | 0.567 | 0.134 | 0.389 | 0.526 | 16.7 | 59.89 |
| Dome-M (weight) | HGNetv2-B2 | 0.382 | 0.607 | 0.401 | 0.302 | 0.489 | 0.623 | 0.142 | 0.417 | 0.556 | 16.13 | 61.98 |
| Dome-L (weight) | HGNetv2-B4 | 0.383 | 0.609 | 0.400 | 0.303 | 0.489 | 0.628 | 0.143 | 0.417 | 0.555 | 14.98 | 66.75 |

> \* DQ-DETR Val 仍为旧 AI-TOD 评估器结果（maxDets=1500, areaRng=verytiny/tiny/small/medium, 无 ignore region 过滤），暂未用新评估器重跑 Val。

## 测试集 (Test, 1609 images)

| Model | Backbone | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **DQ-DETR** | R-50 | **0.257** | **0.436** | **0.263** | **0.163** | **0.342** | **0.463** | **0.102** | **0.331** | **0.468** | 2.70 | 370.4 |
| Dome-DETR Baseline | HGNetv2-B2 | 0.291 | 0.486 | 0.297 | 0.191 | 0.397 | 0.515 | 0.107 | 0.344 | 0.476 | 15.2 | 66.0 |
| Dome-DETR Dome-M | HGNetv2-B2 | 0.289 | 0.485 | 0.296 | 0.191 | 0.394 | 0.515 | 0.105 | 0.343 | 0.480 | 15.3 | 65.4 |
| Dome-S (weight) | HGNetv2-B0 | 0.266 | 0.452 | 0.270 | 0.169 | 0.369 | 0.511 | 0.101 | 0.325 | 0.452 | 16.7 | 59.89 |
| Dome-M (weight) | HGNetv2-B2 | 0.291 | 0.489 | 0.297 | 0.190 | 0.401 | 0.528 | 0.108 | 0.347 | 0.479 | 16.13 | 61.98 |
| Dome-L (weight) | HGNetv2-B4 | 0.293 | 0.493 | 0.298 | 0.189 | 0.401 | 0.536 | 0.109 | 0.346 | 0.477 | 14.98 | 66.75 |

> DQ-DETR Test 使用新 **VisdroneCocoEvaluator** 评估（与 Dome-DETR 对齐），Val 待重跑。
> DQ-DETR FPS/Latency 为 RTX 4060 Ti 实测，Dome-DETR 为原文报告值，不可直接对比。

---
# DQ-DETR

> 评估器: **VisdroneCocoEvaluator** (Test) / 旧 AI-TOD CocoEvaluator (Val)
> Checkpoint: `DQDETR_visdrone_36epoch_ccm_10_50_100_10cls/checkpoint0023.pth`

## 验证集 — 旧评估器 (Val, 548 images)

```
IoU metric: bbox
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=1500 ] = 0.359
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.589
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=1500 ] = 0.366
Average Precision  (AP) @[ IoU=0.50:0.95 | area=verytiny | maxDets=1500 ] = 0.106
Average Precision  (AP) @[ IoU=0.50:0.95 | area=  tiny | maxDets=1500 ] = 0.208
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=1500 ] = 0.337
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=1500 ] = 0.480
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.136
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.578
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=1500 ] = 0.589
Average Recall     (AR) @[ IoU=0.50:0.95 | area=verytiny | maxDets=1500 ] = 0.294
Average Recall     (AR) @[ IoU=0.50:0.95 | area=  tiny | maxDets=1500 ] = 0.458
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=1500 ] = 0.582
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=1500 ] = 0.696
Optimal LRP             @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.715
Optimal LRP Loc         @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.180
Optimal LRP FP          @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.340
Optimal LRP FN          @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.448
# Class-specific LRP-Optimal Thresholds #
 [0.366 0.347 0.347 0.38  0.368 0.363 0.314 0.272 0.285 0.346]
Val:  548 images, FPS=6.20, Latency=161.4ms/image
```

## 测试集 — 新 VisdroneCocoEvaluator (Test, 1609 images)

```
IoU metric: bbox
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=500 ] = 0.257
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=500 ] = 0.436
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=500 ] = 0.263
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=500 ] = 0.163
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=500 ] = 0.342
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=500 ] = 0.463
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.102
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.331
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.468
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=500 ] = 0.474
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=500 ] = 0.390
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=500 ] = 0.567
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=500 ] = 0.624
Test: 1609 images, FPS=2.70, Latency=370.4ms/image (RTX 4060 Ti)
```

# Dome-DETR

> 模型: Baseline Dome-M vs Dome-M | 评估配置: maxDets=[1,10,100,300]

## 验证集 (Val, 548 images, 10 classes)

| Model | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baseline Dome-M | 0.378 | 0.592 | 0.397 | 0.298 | 0.481 | 0.595 | 0.139 | 0.412 | 0.549 | 0.818 | 1222.8 |
| Dome-M | 0.375 | 0.590 | 0.398 | 0.294 | 0.478 | 0.575 | 0.142 | 0.414 | 0.553 | 0.777 | 1287.7 |

### Baseline Dome-M — Val 原始输出
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.378
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.592
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.397
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.298
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.481
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.595
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.139
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.412
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.549
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.486
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.647
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.747
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.831
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.588
```

### Dome-M — Val 原始输出
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.375
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.590
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.398
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.294
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.478
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.575
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.142
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.414
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.553
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.490
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.648
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.733
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.838
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.594
```

## 测试集 (Test, 1609 images, 10 classes)

| Model | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baseline Dome-M | 0.291 | 0.486 | 0.297 | 0.191 | 0.397 | 0.515 | 0.107 | 0.344 | 0.476 | 66.0 | 15.15 |
| Dome-M | 0.289 | 0.485 | 0.296 | 0.191 | 0.394 | 0.515 | 0.105 | 0.343 | 0.480 | 65.36 | 15.3 |

### Baseline Dome-M — Test 原始输出
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.291
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.486
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.297
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.191
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.397
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.515
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.107
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.344
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.476
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.396
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.595
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.697
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.770
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.498
```

### Dome-M — Test 原始输出
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.289
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.485
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.296
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.191
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.394
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.515
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.105
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.343
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.480
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.400
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.600
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.672
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.778
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.503
```


# Dome-DETR 预训练权重 (S/M/L)

> 权重目录: `weight/dome-{s,m,l}-visdrone_converted.pth` | 评估配置: maxDets=[1,10,100,300]

## 验证集 (Val, 548 images, 10 classes)

| Model | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Dome-S (HGNetv2-B0) | 0.347 | 0.561 | 0.360 | 0.269 | 0.451 | 0.567 | 0.134 | 0.389 | 0.526 | 13.05 | 76.6 |
| Dome-M (HGNetv2-B2) | 0.382 | 0.607 | 0.401 | 0.302 | 0.489 | 0.623 | 0.142 | 0.417 | 0.556 | 12.18 | 82.1 |
| Dome-L (HGNetv2-B4) | 0.383 | 0.609 | 0.400 | 0.303 | 0.489 | 0.628 | 0.143 | 0.417 | 0.555 | 11.91 | 83.9 |

原始 COCO 输出

**Dome-S**

```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.347
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.561
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.360
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.269
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.451
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.567
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.134
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.389
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.526
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.457
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.628
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.754
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.818
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.558
```

**Dome-M**
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.382
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.607
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.401
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.302
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.489
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.623
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.142
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.417
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.556
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.494
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.655
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.773
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.848
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.596
```

**Dome-L**
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.383
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.609
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.400
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.303
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.489
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.628
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.143
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.417
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.555
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.493
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.655
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.773
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.849
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.592
```

## 测试集 (Test, 1609 images, 10 classes)

| Model | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Dome-S (HGNetv2-B0) | 0.266 | 0.452 | 0.270 | 0.169 | 0.369 | 0.511 | 0.101 | 0.325 | 0.452 | 14.90 | 67.1 |
| Dome-M (HGNetv2-B2) | 0.291 | 0.489 | 0.297 | 0.190 | 0.401 | 0.528 | 0.108 | 0.347 | 0.479 | 13.75 | 72.7 |
| Dome-L (HGNetv2-B4) | 0.293 | 0.493 | 0.298 | 0.189 | 0.401 | 0.536 | 0.109 | 0.346 | 0.477 | 13.41 | 74.6 |

**原始 COCO 输出**

**Dome-S**

```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.266
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.452
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.270
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.169
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.369
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.511
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.101
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.325
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.452
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.368
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.576
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.670
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.747
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.468
```

**Dome-M**
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.291
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.489
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.297
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.190
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.401
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.528
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.108
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.347
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.479
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.391
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.606
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.686
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.776
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.501
```

**Dome-L**
```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=300 ] = 0.293
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.493
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.298
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.189
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.401
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.536
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.109
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.346
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.477
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=300 ] = 0.387
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=300 ] = 0.601
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=300 ] = 0.687
Average Recall     (AR) @[ IoU=0.50      | area=   all | maxDets=300 ] = 0.774
Average Recall     (AR) @[ IoU=0.75      | area=   all | maxDets=300 ] = 0.494
```
