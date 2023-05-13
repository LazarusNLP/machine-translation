from argparse import ArgumentParser
import json
import os

import evaluate
import torch
from datasets import load_dataset, Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# ISO639-3 to BCP-47
ISO2BCP = {
    "ind": "ind_Latn",
    "ace": "ace_Latn",
    "ban": "ban_Latn",
    "bug": "bug_Latn",
    "jav": "jav_Latn",
    "min": "min_Latn",
    "sun": "sun_Latn",
}


def log_results(result: Dataset, args):
    model_id = args.model.split("/")[-1]

    sacrebleu = evaluate.load("sacrebleu")
    sacrebleu_result = sacrebleu.compute(
        references=result["target"], predictions=result["prediction"]
    )

    result_str = f"SacreBLEU: {round(sacrebleu_result['score'], 2)}"
    print(result_str)

    logging_dir = f"{args.logging_dir}/{model_id}"
    os.makedirs(logging_dir, exist_ok=True)

    with open(f"{logging_dir}/metrics_{args.source}_{args.target}.txt", "w") as f:
        f.write(result_str)

    with open(f"{logging_dir}/log_{args.source}_{args.target}.json", "w") as f:
        data = [
            {"prediction": p, "target": t}
            for p, t in zip(result["prediction"], result["target"])
        ]
        json.dump(data, f, indent=2, ensure_ascii=True)


def indomt5_preprocess(batch, source_text_column_name: str, target_language: str):
    text = batch[source_text_column_name]
    batch[source_text_column_name] = f"<{target_language}>{text}"
    return batch


def main(args):
    dataset = load_dataset(
        args.dataset_name, name=args.dataset_config_name, split="test"
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(args.model)
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    src_lang, tgt_lang = args.source, args.target

    if args.model_type == "nllb":
        src_lang = ISO2BCP[args.source]
        tgt_lang = ISO2BCP[args.target]
    elif args.model_type == "indomt5":
        dataset = dataset.map(
            indomt5_preprocess,
            fn_kwargs={
                "source_text_column_name": args.source_text_column_name,
                "target_language": tgt_lang,
            },
        )

    translator = pipeline(
        "translation",
        model=model,
        tokenizer=tokenizer,
        src_lang=src_lang,
        tgt_lang=tgt_lang,
        device=0 if torch.cuda.is_available() else -1,
    )

    def infer(batch):
        predictions = [
            out["translation_text"]
            for out in translator(
                batch[args.source_text_column_name],
                batch_size=args.batch_size,
                max_length=args.max_length,
                num_beams=args.num_beams,
            )
        ]
        batch["prediction"] = predictions
        batch["target"] = batch[args.target_text_column_name]
        return batch

    result = dataset.map(infer, batched=True, batch_size=args.batch_size)
    log_results(result, args)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="HuggingFace translation model checkpoint.",
    )
    parser.add_argument(
        "--model_type",
        default="indomt5",
        const="indomt5",
        nargs="?",
        choices=["indomt5", "nllb"],
    )
    parser.add_argument(
        "--dataset_name",
        type=str,
        required=True,
        help="The name of the dataset to use.",
    )
    parser.add_argument(
        "--dataset_config_name",
        type=str,
        required=True,
        help="The configuration name of the dataset to use.",
    )
    parser.add_argument(
        "--source", type=str, required=True, help="Source language ISO code."
    )
    parser.add_argument(
        "--target", type=str, required=True, help="Target language ISO code."
    )
    parser.add_argument(
        "--source_text_column_name",
        type=str,
        required=True,
        help="Source text column name in dataset.",
    )
    parser.add_argument(
        "--target_text_column_name",
        type=str,
        required=True,
        help="Target text column name in dataset.",
    )
    parser.add_argument(
        "--max_length",
        type=int,
        required=True,
        help="Maximum length of the sequence to be generated.",
    )
    parser.add_argument(
        "--num_beams",
        type=int,
        default=1,
        help="Number of beams for beam search. 1 means no beam search.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=1,
        help="Batch size for inference.",
    )
    parser.add_argument(
        "--logging_dir", type=str, default="logs", help="Path to logging directory."
    )
    args = parser.parse_args()
    main(args)
