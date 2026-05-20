# DQ-DETR 详细评估

> 评估器: **VisdroneCocoEvaluator** (Val + Test)
> Checkpoint: `DQDETR_visdrone_36epoch_ccm_10_50_100_10cls/checkpoint0023.pth`

## 验证集 — VisdroneCocoEvaluator (Val, 548 images)

```
IoU metric: bbox
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=500 ] = 0.323
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=500 ] = 0.520
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=500 ] = 0.333
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=500 ] = 0.244
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=500 ] = 0.412
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=500 ] = 0.531
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.132
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.384
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.526
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=500 ] = 0.532
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=500 ] = 0.467
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=500 ] = 0.613
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=500 ] = 0.706
Val:  548 images, FPS=6.1, Latency=161.4ms/image (RTX 4090)
```

## 测试集 — VisdroneCocoEvaluator (Test, 1609 images)

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
Test: 1609 images, FPS=6.1, Latency=161.4ms/image (RTX 4090)
```

## 评估器对比验证

对同一 checkpoint 进行三次评估，验证新旧评估器差异来源。

**注意：** 旧 AI-TOD 评估器 areaRng 为 verytiny/tiny/small/medium，新 Visdrone 评估器为 small/medium/large，**面积标签名称相同但范围完全不同**（如旧 small=16²~32² vs 新 small=<32²），因此 AP_S/M/L 不可跨评估器对比。

### 全指标对比 (Test, 1609 images)

| 指标 | 旧 AI-TOD | 新 VisDrone (无过滤) | 新 VisDrone (有过滤) | 过滤影响 |
|------|:---------:|:-------------------:|:-------------------:|:--------:|
| AP (all) | 0.276 | 0.276 | 0.257 | −0.019 |
| AP_50 | 0.481 | 0.481 | 0.436 | −0.045 |
| AP_75 | 0.276 | 0.276 | 0.263 | −0.013 |
| AP_S | — | 0.178 | 0.163 | −0.015 |
| AP_M | — | 0.388 | 0.342 | −0.046 |
| AP_L | — | 0.515 | 0.463 | −0.052 |
| AR@1 | 0.104 | 0.104 | 0.102 | −0.002 |
| AR@10 | — | 0.343 | 0.331 | −0.012 |
| AR@100 | 0.498 | 0.498 | 0.468 | −0.030 |
| AR@500/1500 | 0.509 | 0.509 | 0.474 | −0.035 |
| AR_S | — | 0.421 | 0.390 | −0.031 |
| AR_M | — | 0.631 | 0.567 | −0.064 |
| AR_L | — | 0.714 | 0.624 | −0.090 |

> 旧 AI-TOD 评估器无 AR@10、AP_S/M/L 面积定义不同无法直接填入。

**结论：**
- 关闭 ignore 过滤后，新旧评估器的 AP / AP_50 / AP_75 / AR@100 / AR_maxDets **完全一致**
- maxDets 差异无影响：`num_select=300` 远小于 500，模型输出不被截断
- 开启 ignore 过滤后，**所有指标均下降**，其中 AR_L 下降最大（−0.090），小目标 AP_S 下降最小（−0.015）
- VisDrone 标注中 `category_id=0` / `iscrowd=1` / `ignore=1` 的区域主要为拥挤/遮挡场景，大目标更容易落入 ignore 区域（例如一辆车的一部分被标记为 ignore 的密集人群遮挡）
