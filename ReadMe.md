# VisDrone 模型总览

> **注意**: DQ-DETR 使用 `maxDets=1500` 评估, Dome-DETR 使用 `maxDets=[1,10,100,300]`, AP 值不完全可比。
> Dome-DETR Baseline/Dome-M 的 Val FPS/Latency 数据缺失。

## 验证集 (Val, 548 images)

| Model | Backbone | AP | AP_50 | AP_75 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|
| **DQ-DETR** | — | 0.359* | 0.589* | 0.366* | 6.20 | 161.4 |
| Dome-DETR Baseline | HGNetv2-B2 | 0.378 | 0.592 | 0.397 | 15.2 | 66.0 |
| Dome-DETR Dome-M | HGNetv2-B2 | 0.375 | 0.590 | 0.398 |  15.3 | 65.4 |
| Dome-S (weight) | HGNetv2-B0 | 0.347 | 0.561 | 0.360 | 16.7 | 59.89 |
| Dome-M (weight) | HGNetv2-B2 | 0.382 | 0.607 | 0.401 | 16.13 | 61.98 |
| Dome-L (weight) | HGNetv2-B4 | 0.383 | 0.609 | 0.400 | 14.98 | 66.75 |

> \* DQ-DETR 使用 maxDets=1500 (vs Dome-DETR maxDets=300)，AP 偏高约 1–2 个点。

## 测试集 (Test, 1609 images)

| Model | Backbone | AP | AP_50 | AP_75 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|
| **DQ-DETR** | — | 0.276* | 0.481* | 0.276* | 7.29 | 137.2 |
| Dome-DETR Baseline | HGNetv2-B2 | 0.291 | 0.486 | 0.297 | 15.2 | 66.0 |
| Dome-DETR Dome-M | HGNetv2-B2 | 0.289 | 0.485 | 0.296 | 15.3 | 65.4 |
| Dome-S (weight) | HGNetv2-B0 | 0.266 | 0.452 | 0.270 | 16.7 | 59.89 |
| Dome-M (weight) | HGNetv2-B2 | 0.291 | 0.489 | 0.297 | 16.13 | 61.98 |
| Dome-L (weight) | HGNetv2-B4 | 0.293 | 0.493 | 0.298 | 14.98 | 66.75 |

> \* DQ-DETR 使用 maxDets=1500，与 Dome-DETR 不完全可比。

---
# DQ-DETR

```
DONE (t=4.79s).
IoU metric: bbox
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=1500 ] = 0.359
Average Precision  (AP) @[ IoU=0.25      | area=   all | maxDets=1500 ] = -1.000
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
Test:  [   0/1609]  eta: 0:25:51    time: 0.9640  data: 0.6607  max mem: 2252
Test:  [1608/1609]  eta: 0:00:00    time: 0.1802  data: 0.0031  max mem: 2252
Test: Total time: 0:06:41 (0.2496 s / it)
Averaged stats: 
Accumulating evaluation results...
DONE (t=14.08s).
IoU metric: bbox
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=1500 ] = 0.276
Average Precision  (AP) @[ IoU=0.25      | area=   all | maxDets=1500 ] = -1.000
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.481
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=1500 ] = 0.276
Average Precision  (AP) @[ IoU=0.50:0.95 | area=verytiny | maxDets=1500 ] = 0.041
Average Precision  (AP) @[ IoU=0.50:0.95 | area=  tiny | maxDets=1500 ] = 0.124
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=1500 ] = 0.239
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=1500 ] = 0.400
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.104
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.498
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=1500 ] = 0.509
Average Recall     (AR) @[ IoU=0.50:0.95 | area=verytiny | maxDets=1500 ] = 0.175
Average Recall     (AR) @[ IoU=0.50:0.95 | area=  tiny | maxDets=1500 ] = 0.353
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=1500 ] = 0.504
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=1500 ] = 0.641
Optimal LRP             @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.775
Optimal LRP Loc         @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.199
Optimal LRP FP          @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.411
Optimal LRP FN          @[ IoU=0.50      | area=   all | maxDets=1500 ] = 0.532
# Class-specific LRP-Optimal Thresholds # 
 [0.37  0.339 0.287 0.385 0.322 0.377 0.357 0.269 0.342 0.345]
Test: 1609 images, FPS=7.29, Latency=137.2ms/image
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
