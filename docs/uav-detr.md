# UAV-DETR 详细评估

> 评估器: VisdroneCocoEvaluator（`get_COCO_metrice.py`，maxDets=[1,10,100,500]）| 速度测试: `speed_test.py`

## 模型配置

| Variant | Backbone | Params | GFLOPs | Config |
|---------|----------|--------|--------|--------|
| UAV-DETR-R50 | ResNet-50 | 44.4M | 161.4 | `ultralytics/cfg/models/uavdetr-r50.yaml` |

## UAV-DETR-R50

> Checkpoint: `uavdetr_r50/exp2/weights/best.pt` | 训练: imgsz=800, epochs=400, batch=2

### COCO 评估

> 标准 COCOeval，maxDets=[1,10,100]

| Split | AP | AP_50 | AP_75 | AP_S | AP_M | AP_L | AR@1 | AR@10 | AR@100 |
|-------|----:|-----:|-----:|-----:|-----:|-----:|-----:|------:|-------:|
| Val (548 imgs) | 0.334 | 0.540 | 0.348 | 0.251 | 0.449 | 0.476 | 0.125 | 0.335 | 0.434 |
| Test (1609 imgs) | 0.256 | 0.436 | 0.259 | 0.156 | 0.360 | 0.462 | 0.098 | 0.278 | 0.360 |

### Ultralytics 内置评估

#### Val (548 images)

```
Class           Images  Instances   Box(P)      R       mAP50   mAP50-95
all             548     38759       0.673       0.556   0.574   0.365
pedestrian      548     8844        0.736       0.602   0.661   0.338
people          548     5125        0.696       0.571   0.592   0.264
bicycle         548     1287        0.559       0.368   0.361   0.181
car             548     14064       0.839       0.867   0.886   0.662
van             548     1975        0.696       0.551   0.587   0.451
truck           548     750         0.673       0.511   0.526   0.365
tricycle        548     1045        0.542       0.490   0.452   0.283
awning-tricycle 548     532         0.428       0.246   0.253   0.168
bus             548     251         0.854       0.701   0.747   0.584
motor           548     4886        0.709       0.656   0.677   0.351
Speed: 0.3ms preprocess, 19.8ms inference, 0.0ms loss, 0.2ms postprocess (batch=4)
```

#### Test (1609 images)

```
Class           Images  Instances   Box(P)      R       mAP50   mAP50-95
all             1609    75082       0.604       0.474   0.463   0.275
pedestrian      1609    21000       0.639       0.447   0.475   0.201
people          1609    6376        0.615       0.326   0.350   0.133
bicycle         1609    1302        0.488       0.257   0.225   0.105
car             1609    28063       0.796       0.821   0.828   0.549
van             1609    5770        0.621       0.470   0.454   0.333
truck           1609    2659        0.593       0.603   0.564   0.378
tricycle        1609    530         0.387       0.436   0.330   0.191
awning-tricycle 1609    599         0.503       0.254   0.247   0.162
bus             1609    2938        0.802       0.588   0.636   0.470
motor           1609    5845        0.598       0.542   0.516   0.231
Speed: 0.2ms preprocess, 15.8ms inference, 0.0ms loss, 0.2ms postprocess (batch=4)
```

### 速度测试 (RTX 4090, FP32, input 800×800)

| Batch | Latency (ms) | FPS | Note |
|------:|-------------:|----:|------|
| 1 | 28.69 | 34.86 | 单图延迟，对齐主表口径 |
| 4 | 16.01 | 62.45 | 整批均摊，对齐 val.py 口径 |

其中，batch=4是为了复现验证时ultralytics给出的inference字段。

```bash
# batch=1（主表口径）
python speed_test.py --weights uavdetr_r50/exp2/weights/best.pt --data ../VisDrone.yaml --imgsz 800

# batch=4（val.py 口径）
python speed_test.py --weights uavdetr_r50/exp2/weights/best.pt --data ../VisDrone.yaml --imgsz 800 --batch 4
```
