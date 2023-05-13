for LANGUAGE in abs ace atq ban bbc bkl blz btd bts btx bug bvz end gbi gor hvn iba jav kgr kzf ljp mad mak mej min mkn mog mqj mqy mvp mwv nia nij npy pmf ppk ptu sas sda sun sxn tby twu yli yva
do
    python src/eval.py \
        --model LazarusNLP/indo-t5-base-v2 \
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
        --model LazarusNLP/indo-t5-base-v2 \
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