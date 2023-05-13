torchrun \
    --nproc_per_node 8 src/run_translation.py \
    --model_name_or_path LazarusNLP/indo-t5-base-v2 \
    --dataset_name LazarusNLP/NusaX-MT \
    --dataset_config_name ALL \
    --output_dir ./indo-t5-base-v2-nusax \
    --per_device_train_batch_size 32 \
    --per_device_eval_batch_size 16 \
    --learning_rate 2e-4 \
    --lr_scheduler_type linear \
    --warmup_ratio 0.1 \
    --max_steps 1500 \
    --evaluation_strategy steps \
    --eval_steps 500 \
    --save_strategy steps \
    --save_steps 1500 \
    --logging_strategy steps \
    --logging_steps 100 \
    --max_source_length 128 \
    --max_target_length 128 \
    --val_max_target_length 128 \
    --pad_to_max_length True \
    --source_text_column_name text_1 \
    --target_text_column_name text_2 \
    --source_lang_column_name text_1_lang \
    --target_lang_column_name text_2_lang \
    --preprocessing_num_workers 6 \
    --overwrite_output_dir \
    --do_train --do_eval \
    --predict_with_generate \
    --bf16 \
    --torch_compile True \
    --optim adamw_torch_fused \
    --report_to tensorboard \
    --push_to_hub \
    --hub_model_id LazarusNLP/indo-t5-base-v2-nusax \
    --hub_private_repo True \
    --use_auth_token