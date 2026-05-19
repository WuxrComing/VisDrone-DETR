#!/bin/bash
# Evaluate a trained checkpoint on both val and test sets
# Usage:
#   bash scripts/eval_val_test.sh <checkpoint_path>              # eval on both val + test-dev
#   bash scripts/eval_val_test.sh <checkpoint_path> [output_dir] [--test]

checkpoint="$1"
output_dir="logs/eval_val_test"
extra_flags=""

shift
while [[ $# -gt 0 ]]; do
    case "$1" in
        --test)
            extra_flags="$extra_flags --test"
            shift
            ;;
        -*)
            extra_flags="$extra_flags $1"
            shift
            ;;
        *)
            output_dir="$1"
            shift
            ;;
    esac
done

if [ -z "$checkpoint" ]; then
    echo "Usage: bash scripts/eval_val_test.sh <checkpoint_path> [output_dir] [--test]"
    echo ""
    echo "Examples:"
    echo "  bash scripts/eval_val_test.sh logs/.../checkpoint0035.pth"
    echo "  bash scripts/eval_val_test.sh logs/.../checkpoint0035.pth --test"
    echo "  bash scripts/eval_val_test.sh logs/.../checkpoint0035.pth logs/my_eval --test"
    exit 1
fi

python main_aitod.py \
    --output_dir "$output_dir" \
    -c config/DQ_5scale.py \
    --coco_path /mnt/nas/DataSet/VisDrone \
    --dataset_file visdrone \
    --eval --resume "$checkpoint" $extra_flags \
    --options dn_scalar=100 embed_init_tgt=False \
    dn_label_coef=1.0 dn_bbox_coef=1.0 use_ema=False \
    dn_box_noise_scale=1.0
