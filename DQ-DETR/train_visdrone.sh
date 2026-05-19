source activate dqdetr

nohup \
python main_aitod.py \
  --output_dir logs/DQDETR_visdrone_24epoch_ccm_10_50_100_10cls \
  -c config/visdrone_config.py \
  --dataset_file visdrone \
  --pretrain_model_path pretrain_model.pth \
  --coco_path /mnt/d/DataSet/VisDrone \
  --options dn_scalar=100 embed_init_tgt=False dn_label_coef=1.0 dn_bbox_coef=1.0 use_ema=False dn_box_noise_scale=1.0 \
  >> DQDETR_visdrone_24epoch_ccm_10_50_100_10cls.log 2>&1 &