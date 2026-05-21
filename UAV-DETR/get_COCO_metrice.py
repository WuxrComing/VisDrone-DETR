"""
VisDrone COCO evaluation — 对齐 Dome-DETR VisdroneCocoEvaluator.

参数:
    maxDets = [1, 10, 100, 500]
    areaRng: all / small(<32²) / medium(32²~96²) / large(>96²)
    13 stats

用法:
    python get_COCO_metrice.py --anno_json /path/to/instances_val.json --pred_json runs/val/exp/predictions.json
"""

import argparse
import numpy as np
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--anno_json', type=str,
                        default='/mnt/nas/DataSet/VisDrone/annotations/instances_val.json')
    parser.add_argument('--pred_json', type=str,
                        default='runs/val/valset/predictions.json')
    return parser.parse_known_args()[0]


def compute_visdrone_stats(coco_eval):
    """从 self.eval 直接读取 precision/recall 数组，计算 13 个 VisDrone 指标。

    precision shape: [T, R, K, A, M]  (T=10 IoU, R=101 recall, K=cats, A=4 area, M=4 maxDets)
    recall shape:    [T, K, A, M]
    """
    p = coco_eval.params
    prec = coco_eval.eval['precision']
    rec = coco_eval.eval['recall']

    # area index
    area_idx = {lbl: i for i, lbl in enumerate(p.areaRngLbl)}  # all=0, small=1, medium=2, large=3
    # maxDets index: [1, 10, 100, 500] -> 0,1,2,3
    md_list = p.maxDets

    def _mean(arr):
        return float(np.mean(arr[arr > -1])) if (arr > -1).any() else -1.0

    stats = np.zeros((13,))

    # AP — precision[ T, R, K, A=area, M=maxdet ]
    stats[0] = _mean(prec[:, :, :, area_idx['all'],   3])   # AP
    stats[1] = _mean(prec[0, :, :, area_idx['all'],   3])   # AP_50  (IoU idx 0 = 0.50)
    stats[2] = _mean(prec[5, :, :, area_idx['all'],   3])   # AP_75  (IoU idx 5 = 0.75)
    stats[3] = _mean(prec[:, :, :, area_idx['small'], 3])   # AP_small
    stats[4] = _mean(prec[:, :, :, area_idx['medium'],3])   # AP_medium
    stats[5] = _mean(prec[:, :, :, area_idx['large'], 3])   # AP_large

    # AR — recall[ T, K, A=area, M=maxdet ]
    stats[6]  = _mean(rec[:, :, area_idx['all'],   0])   # AR@1
    stats[7]  = _mean(rec[:, :, area_idx['all'],   1])   # AR@10
    stats[8]  = _mean(rec[:, :, area_idx['all'],   2])   # AR@100
    stats[9]  = _mean(rec[:, :, area_idx['all'],   3])   # AR@500
    stats[10] = _mean(rec[:, :, area_idx['small'], 3])   # AR_small
    stats[11] = _mean(rec[:, :, area_idx['medium'],3])   # AR_medium
    stats[12] = _mean(rec[:, :, area_idx['large'], 3])   # AR_large

    return stats


def main():
    opt = parse_opt()
    print(f"GT:  {opt.anno_json}")
    print(f"Pred: {opt.pred_json}")

    anno = COCO(opt.anno_json)
    pred = anno.loadRes(opt.pred_json)

    # --- standard COCO eval (with VisDrone params) ---
    coco_eval = COCOeval(anno, pred, 'bbox')
    coco_eval.params.maxDets = [1, 10, 100, 500]
    # areaRng 默认就是 all/small/medium/large (<32², 32²~96², >96²)，与 VisDrone 一致

    coco_eval.evaluate()
    coco_eval.accumulate()
    coco_eval.summarize()

    # --- VisDrone 13 stats ---
    stats = compute_visdrone_stats(coco_eval)
    labels = [
        "AP (all)          ",
        "AP_50             ",
        "AP_75             ",
        "AP_small          ",
        "AP_medium         ",
        "AP_large          ",
        "AR@1              ",
        "AR@10             ",
        "AR@100            ",
        "AR@500            ",
        "AR_small          ",
        "AR_medium         ",
        "AR_large          ",
    ]
    print("\n--- VisDrone 13 stats (for docs) ---")
    for label, val in zip(labels, stats):
        print(f"{label} = {val:.3f}")

    # --- TIDE error analysis (optional) ---
    try:
        from tidecv import TIDE, datasets
        tide = TIDE()
        tide.evaluate_range(datasets.COCO(opt.anno_json),
                            datasets.COCOResult(opt.pred_json), mode=TIDE.BOX)
        tide.summarize()
        tide.plot(out_dir='tide_result')
    except ImportError:
        print("\n[TIDE not installed, skipping]")
    except Exception as e:
        print(f"\n[TIDE error: {e}]")


if __name__ == '__main__':
    main()
