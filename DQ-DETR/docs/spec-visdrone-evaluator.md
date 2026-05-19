# Spec: 为 DQ-DETR 增加 VisDrone 专用评估器

## 背景

### 当前状态

DQ-DETR 目前对**所有数据集**（coco / aitod / visdrone）使用同一个 `CocoEvaluator`（`datasets/coco_eval.py`），该评估器基于 `aitodpycocotools`（即 `cocoapi-aitod` 源码），内置了 AI-TOD 数据集的特征：

| 参数 | 当前值（DQ-DETR） | 说明 |
|------|-------------------|------|
| maxDets | `[1, 100, 1500]` | AI-TOD 默认 |
| areaRng | all / verytiny / tiny / small / medium | AI-TOD 四档面积 |
| areaRngLbl | `['all', 'verytiny', 'tiny', 'small', 'medium']` | |
| stats 数量 | **19** | 含 LRP-Error 5 项 |
| 忽略区域过滤 | **无** | |

这意味着当用 DQ-DETR 评估 VisDrone 数据集时，实际使用的是 AI-TOD 的面积划分标准，且没有过滤 VisDrone 标注中的忽略区域。

### 目标状态（对标 Dome-DETR）

Dome-DETR 为 VisDrone 提供了专用评估器 `VisdroneCocoEvaluator`（`src/data/dataset/coco_eval_visdrone.py`），参数如下：

| 参数 | Dome-DETR VisdroneCocoEvaluator |
|------|-------------------------------|
| maxDets | `[1, 10, 100, 500]` |
| areaRng | all / small(`[0², 32²]`) / medium(`[32², 96²]`) / large(`[96², 1e5²]`) |
| areaRngLbl | `['all', 'small', 'medium', 'large']` |
| stats 数量 | **13**（无 LRP-Error） |
| 忽略区域过滤 | **有**（IoF threshold = 0.5） |
| cleanup() | **有**（支持多次评估） |
| 后端 | `faster_coco_eval`（C++ 加速） |

### 为什么需要这个改动

1. AI-TOD 的面积划分（verytiny < 8², tiny 8²~16², small 16²~32²）与 VisDrone 不匹配，导致 AP 按面积统计的结果无法与 Dome-DETR 或其他 VisDrone 方法对比
2. VisDrone 标注文件中存在 `ignore=1` 或 `category_id=0` 的忽略区域，不处理会导致这些区域的检测被错误计入 FP
3. LRP-Error 指标不是 VisDrone 标准评估的一部分，输出格式与 Dome-DETR 不一致

---

## 约束条件

1. **必须保持 `aitodpycocotools` 作为后端**——DQ-DETR 依赖它，不引入 `faster_coco_eval` 新依赖
2. **不得影响现有 AI-TOD 评估流程**——通过 `args.dataset_file` 判断走哪个评估器
3. **`aitodpycocotools.cocoeval.COCOeval` 的关键差异**：
   - 没有 `separate_eval` 参数
   - 没有 `_evalImgs_cpp` 属性（使用 `evalImgs`）
   - `accumulate()` 硬编码 `with_lrp=True`，始终计算 LRP
   - `summarize()` 硬编码引用 `'verytiny'/'tiny'` 面积标签
   - `loadRes` 是类方法，不是实例方法

---

## 设计方案

### 整体架构

```
datasets/
  coco_eval.py            ← 现有 CocoEvaluator（AI-TOD / 通用，不变）
  coco_eval_visdrone.py   ← 新增 VisdroneCocoEvaluator
engine.py                 ← 修改：根据 dataset_file 选择评估器
```

### 关键设计决策

**决策 1：后端选择**
保持 `aitodpycocotools`，通过子类化 `COCOeval` + 覆盖 `summarize()` 来适配 VisDrone。不引入 `faster_coco_eval`。

**原因**：DQ-DETR 已依赖 `aitodpycocotools`，用户已下载 `cocoapi-aitod` 源码。换后端会引入不必要的依赖复杂度。

**决策 2：summarize() 覆盖**
子类化 `COCOeval` 为 `VisdroneCOCOeval`，覆盖 `summarize()` 输出 13 个 stats（对标 Dome-DETR），不显示 LRP。在 `__init__` 中设置 `areaRngLbl = ['all', 'small', 'medium', 'large']` 供 `_summarize()` 内部解析。

**决策 3：evaluate() 函数**
在 `coco_eval_visdrone.py` 中复制一份独立的 `evaluate(self)` 函数（与 `coco_eval.py:221-267` 相同逻辑）。它从 `self.params` 动态读取参数，因此 VisDrone 参数会自动生效。

**决策 4：分布式合并逻辑**
使用 DQ-DETR 已有的 `merge()` 模式（`util.misc.all_gather()` + `evalImgs` numpy 数组），而非 Dome-DETR 的 `_evalImgs_cpp` + `.tolist()` 路径。两个项目在此处的底层逻辑一致，无需改变。

**决策 5：LRP 计算**
`aitodpycocotools` 的 `accumulate()` 无法跳过 LRP 计算（硬编码 `with_lrp=True`），因此 LRP 数据仍然在 `self.eval` dict 中，但我们的 `summarize()` 覆盖不输出它。性能影响可忽略。

---

## 实施步骤

### 步骤 1：创建 `datasets/coco_eval_visdrone.py`

新文件，约 350 行，包含以下模块（按依赖顺序）：

**1a. 导入**
```python
import contextlib, copy, os, numpy as np, torch
from aitodpycocotools.cocoeval import COCOeval
from aitodpycocotools.coco import COCO
import aitodpycocotools.mask as mask_util
from util.misc import all_gather
```

**1b. 辅助函数**（对照 `coco_eval.py` 和 Dome-DETR 的 `coco_eval_visdrone.py`）

| 函数 | 来源 | 说明 |
|------|------|------|
| `convert_to_xywh(boxes)` | `coco_eval.py:178-180` | 坐标转换，完全复用 |
| `detections_in_ignore_regions(boxes, ignore_boxes, iof_threshold)` | Dome-DETR `coco_eval_visdrone.py:338-352` | IoF 过滤，完全复用 |
| `merge(img_ids, eval_imgs)` | `coco_eval.py:183-202` | 分布式合并，使用 `all_gather` |
| `create_common_coco_eval(...)` | `coco_eval.py:205-212` | 合并后赋值给 COCOeval |
| `evaluate(self)` | `coco_eval.py:221-267` | 独立 evaluate 函数，动态读取 `self.params` |

**1c. `VisdroneCOCOeval(COCOeval)` 子类**
```python
class VisdroneCOCOeval(COCOeval):
    def __init__(self, coco_gt, iouType):
        super().__init__(coco_gt, iouType=iouType)
        # 覆盖为 VisDrone 参数
        self.params.maxDets = [1, 10, 100, 500]
        self.params.areaRng = [
            [0**2, 1e5**2],    # all
            [0**2, 32**2],     # small
            [32**2, 96**2],    # medium
            [96**2, 1e5**2],   # large
        ]
        self.params.areaRngLbl = ['all', 'small', 'medium', 'large']

    def summarize(self):
        # 覆盖：输出 13 stats，对标 Dome-DETR，无 LRP
```

`summarize()` 的 `_summarizeDets()` 输出：

| 索引 | 指标 | 说明 |
|------|------|------|
| 0 | AP @ IoU=0.50:0.95 | all area, maxDets=500 |
| 1 | AP @ IoU=0.50 | |
| 2 | AP @ IoU=0.75 | |
| 3 | AP @ small | area < 32² |
| 4 | AP @ medium | 32² ≤ area < 96² |
| 5 | AP @ large | area ≥ 96² |
| 6 | AR @ maxDets=1 | |
| 7 | AR @ maxDets=10 | |
| 8 | AR @ maxDets=100 | |
| 9 | AR @ maxDets=500 | |
| 10 | AR @ small | |
| 11 | AR @ medium | |
| 12 | AR @ large | |

`self.stats = self.all_stats[:12]`

**1d. `VisdroneCocoEvaluator` 类**

```python
class VisdroneCocoEvaluator(object):
    def __init__(self, coco_gt, iou_types, useCats=True, ignore_iof_threshold=0.5):
        # 1. 收集忽略区域 _collect_ignore_regions(coco_gt)
        # 2. 为每个 iou_type 创建 VisdroneCOCOeval
        # 3. 初始化 img_ids, eval_imgs

    def cleanup(self):
        # 重置所有状态，支持多次评估

    def update(self, predictions):
        # 1. prepare() → prepare_for_coco_detection() 中过滤忽略区域
        # 2. COCO.loadRes()
        # 3. 调用独立 evaluate() 函数
        # 4. 收集 eval_imgs

    def synchronize_between_processes(self):
        # 同 coco_eval.py:58-61

    def accumulate(self):
        # 调用 coco_eval.accumulate()（内部仍计算 LRP）

    def summarize(self):
        # 调用 coco_eval.summarize()（覆盖版，只输出 13 stats）

    def _collect_ignore_regions(self, coco_gt):
        # 照搬 Dome-DETR coco_eval_visdrone.py:252-269
        # 收集 category_id==0 或 iscrowd==1 或 ignore==1 的标注
```

`prepare_for_coco_detection()` 中的忽略区域过滤逻辑（对照 Dome-DETR:212-249）：
```python
def prepare_for_coco_detection(self, predictions):
    coco_results = []
    for original_id, prediction in predictions.items():
        if len(prediction) == 0:
            continue
        boxes = prediction["boxes"]
        scores = prediction["scores"]
        labels = prediction["labels"]

        # 过滤忽略区域
        ignore_boxes = self.ignore_regions.get(original_id)
        if ignore_boxes is not None and len(boxes) > 0:
            keep = ~detections_in_ignore_regions(
                boxes, ignore_boxes.to(boxes.device), self.ignore_iof_threshold
            )
            boxes = boxes[keep]
            scores = scores[keep]
            labels = labels[keep]

        if len(boxes) == 0:
            continue
        # ... 后续转换为 COCO 格式
```

### 步骤 2：修改 `engine.py`

**位置**：第 165 行附近（`CocoEvaluator` 实例化处）

**当前代码**：
```python
coco_evaluator = CocoEvaluator(base_ds, iou_types, useCats=useCats)
```

**改为**：
```python
if args is not None and hasattr(args, 'dataset_file') and args.dataset_file == 'visdrone':
    from datasets.coco_eval_visdrone import VisdroneCocoEvaluator
    coco_evaluator = VisdroneCocoEvaluator(base_ds, iou_types, useCats=useCats)
else:
    coco_evaluator = CocoEvaluator(base_ds, iou_types, useCats=useCats)
```

`evaluate()` 函数中其他代码不受影响——`coco_evaluator` 变量名不变，下游的 `update()`/`synchronize_between_processes()`/`accumulate()`/`summarize()` 接口完全一致。

---

## 改动影响评估

| 评估路径 | 改动前 | 改动后 | 影响 |
|----------|--------|--------|------|
| AI-TOD 评估 | `CocoEvaluator` | `CocoEvaluator`（else 分支） | **无影响** |
| COCO 评估 | `CocoEvaluator` | `CocoEvaluator`（else 分支） | **无影响** |
| VisDrone 评估 | `CocoEvaluator` | `VisdroneCocoEvaluator`（if 分支） | **参数变化** |

VisDrone 评估的具体变化：

| 指标 | 改动前 | 改动后 |
|------|--------|--------|
| areaRng 划分 | verytiny/tiny/small/medium | small/medium/large |
| maxDets | [1, 100, 1500] | [1, 10, 100, 500] |
| stats 数量 | 19（含 LRP） | 13（无 LRP） |
| 忽略区域过滤 | 无 | 有（IoF=0.5） |
| AP_all / AP_50 / AP_75 | 一致 | 一致 |
| stats[0] 对应的 mAP | 相同（都是 all area, maxDets[-1]） | ⚠️ maxDets 从 1500→500，结果可能略有不同 |

⚠️ **注意**：由于 DQ-DETR 的后处理保留了 `num_select` 个检测框（通常默认是 300），所以 `maxDets` 从 1500 改为 500 **对最终 mAP 无实际影响**——实际检测数远小于 500。

---

## 验证方式

1. **语法检查**：
   ```bash
   cd /mnt/nas/Programming/VisDrone-DETR/DQ-DETR
   python -c "from datasets.coco_eval_visdrone import VisdroneCocoEvaluator; print('OK')"
   ```

2. **导入兼容性**：确认 `CocoEvaluator` 仍能正常导入
   ```bash
   python -c "from datasets.coco_eval import CocoEvaluator; print('OK')"
   ```

3. **端到端测试**（需 GPU + VisDrone 数据）：
   ```bash
   bash scripts/eval_val_test.sh
   ```
   对比输出 stats 数量从 19 → 13，且面积标签从 verytiny/tiny/small/medium → small/medium/large

4. **回归测试**：运行 AI-TOD 评估确认无变化
   ```bash
   bash scripts/DQ_eval.sh
   ```
