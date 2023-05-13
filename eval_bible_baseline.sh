for LANGUAGE in ace ban bug jav min sun
do
    python src/eval.py \
        --model LazarusNLP/indo-t5-base \
        --model_type indomt5 \
        --dataset_name LazarusNLP/alkitab-sabda-mt \
        --dataset_config_name ind-$LANGUAGE \
        --source ind \
        --target $LANGUAGE \
        --source_text_column_name text_source \
        --target_text_column_name text_target \
        --max_length 400 \
        --num_beams 10 \
        --batch_size 32
    
    python src/eval.py \
        --model LazarusNLP/indo-t5-base \
        --model_type indomt5 \
        --dataset_name LazarusNLP/alkitab-sabda-mt \
        --dataset_config_name $LANGUAGE-ind \
        --source $LANGUAGE \
        --target ind \
        --source_text_column_name text_source \
        --target_text_column_name text_target \
        --max_length 400 \
        --num_beams 10 \
        --batch_size 32
done