# Dome-DETR 详细评估

> 模型: Baseline (w/o Dome) vs Dome-DETR-M | 评估配置: maxDets=[1,10,100,300]
>
> **说明**: 二者均使用 HGNetv2-B2 骨干，Baseline 无 Dome 模块，Dome-DETR-M 有 Dome 模块，对比反映 Dome 模块效果。

## Baseline (w/o Dome)

### 验证集 (Val, 548 images)

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

### 测试集 (Test, 1609 images)

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

## Dome-DETR-M

### 验证集 (Val, 548 images)

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

### 测试集 (Test, 1609 images)

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

## Dome-DETR 预训练权重 (S / M / L)

> 权重目录: `weight/dome-{s,m,l}-visdrone_converted.pth` | 评估配置: maxDets=[1,10,100,300]

### 验证集 (Val, 548 images)

| Model | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Dome-DETR-S (HGNetv2-B0) | 0.347 | 0.561 | 0.360 | 0.269 | 0.451 | 0.567 | 0.134 | 0.389 | 0.526 | 13.05 | 76.6 |
| Dome-DETR-M (HGNetv2-B2) | 0.382 | 0.607 | 0.401 | 0.302 | 0.489 | 0.623 | 0.142 | 0.417 | 0.556 | 12.18 | 82.1 |
| Dome-DETR-L (HGNetv2-B4) | 0.383 | 0.609 | 0.400 | 0.303 | 0.489 | 0.628 | 0.143 | 0.417 | 0.555 | 11.91 | 83.9 |

#### Dome-DETR-S Val 原始输出

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

#### Dome-DETR-M Val 原始输出

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

#### Dome-DETR-L Val 原始输出

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

### 测试集 (Test, 1609 images)

| Model | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 | FPS | Latency(ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Dome-DETR-S (HGNetv2-B0) | 0.266 | 0.452 | 0.270 | 0.169 | 0.369 | 0.511 | 0.101 | 0.325 | 0.452 | 14.90 | 67.1 |
| Dome-DETR-M (HGNetv2-B2) | 0.291 | 0.489 | 0.297 | 0.190 | 0.401 | 0.528 | 0.108 | 0.347 | 0.479 | 13.75 | 72.7 |
| Dome-DETR-L (HGNetv2-B4) | 0.293 | 0.493 | 0.298 | 0.189 | 0.401 | 0.536 | 0.109 | 0.346 | 0.477 | 13.41 | 74.6 |

#### Dome-DETR-S Test 原始输出

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

#### Dome-DETR-M Test 原始输出

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

#### Dome-DETR-L Test 原始输出

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
