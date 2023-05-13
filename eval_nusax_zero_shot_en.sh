for LANGUAGE in ace ban bbc bjn bug ind jav mad min nij sun
do
    python src/eval.py \
        --model LazarusNLP/indo-t5-base-v2-nusax \
        --model_type indomt5 \
        --dataset_name indonlp/NusaX-MT \
        --dataset_config_name eng-$LANGUAGE \
        --source eng \
        --target $LANGUAGE \
        --source_text_column_name text_1 \
        --target_text_column_name text_2 \
        --max_length 400 \
        --num_beams 10 \
        --batch_size 32
done