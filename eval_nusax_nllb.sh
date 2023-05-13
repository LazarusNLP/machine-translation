for LANGUAGE in ace ban bug jav min sun
do
    python src/eval.py \
        --model facebook/nllb-200-distilled-600M \
        --model_type nllb \
        --dataset_name indonlp/NusaX-MT \
        --dataset_config_name ind-$LANGUAGE \
        --source ind \
        --target $LANGUAGE \
        --source_text_column_name text_1 \
        --target_text_column_name text_2 \
        --max_length 400 \
        --num_beams 10 \
        --batch_size 16
    
    python src/eval.py \
        --model facebook/nllb-200-distilled-600M \
        --model_type nllb \
        --dataset_name indonlp/NusaX-MT \
        --dataset_config_name $LANGUAGE-ind \
        --source $LANGUAGE \
        --target ind \
        --source_text_column_name text_1 \
        --target_text_column_name text_2 \
        --max_length 400 \
        --num_beams 10 \
        --batch_size 16
done