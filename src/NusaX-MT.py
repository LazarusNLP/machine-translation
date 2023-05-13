# Modified from https://huggingface.co/datasets/indonlp/NusaX-MT/blob/main/NusaX-MT.py
# We modified the data loading script by removing English
# and providing BASELINE LANGUAGES config

from pathlib import Path
from typing import Dict, List, Tuple

import datasets
import pandas as pd

_DATASETNAME = "NusaX_MT"

_LANGUAGES = [
    "ind",
    "ace",
    "ban",
    "bjn",
    "bbc",
    "bug",
    "jav",
    "mad",
    "min",
    "nij",
    "sun",
]  # We follow ISO639-3 language code (https://iso639-3.sil.org/code_tables/639/data)
_BASELINE_LANGUAGES = ["ace", "ban", "bug", "ind", "jav", "min", "sun"]
_LOCAL = False

_CITATION = """\
@misc{winata2022nusax,
      title={NusaX: Multilingual Parallel Sentiment Dataset for 10 Indonesian Local Languages},
      author={Winata, Genta Indra and Aji, Alham Fikri and Cahyawijaya,
      Samuel and Mahendra, Rahmad and Koto, Fajri and Romadhony,
      Ade and Kurniawan, Kemal and Moeljadi, David and Prasojo,
      Radityo Eko and Fung, Pascale and Baldwin, Timothy and Lau,
      Jey Han and Sennrich, Rico and Ruder, Sebastian},
      year={2022},
      eprint={2205.15960},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
"""

_DESCRIPTION = """\
NusaX is a high-quality multilingual parallel corpus that covers 12 languages, Indonesian, English, and 10 Indonesian local languages, namely Acehnese, Balinese, Banjarese, Buginese, Madurese, Minangkabau, Javanese, Ngaju, Sundanese, and Toba Batak.
NusaX-MT is a parallel corpus for training and benchmarking machine translation models across 10 Indonesian local languages + Indonesian and English. The data is presented in csv format with 12 columns, one column for each language.
"""

_HOMEPAGE = "https://github.com/IndoNLP/nusax/tree/main/datasets/mt"

_LICENSE = "Creative Commons Attribution Share-Alike 4.0 International"

_SOURCE_VERSION = "1.0.0"

_URLS = {
    "train": "https://raw.githubusercontent.com/IndoNLP/nusax/main/datasets/mt/train.csv",
    "validation": "https://raw.githubusercontent.com/IndoNLP/nusax/main/datasets/mt/valid.csv",
    "test": "https://raw.githubusercontent.com/IndoNLP/nusax/main/datasets/mt/test.csv",
}

LANGUAGES_MAP = {
    "ace": "acehnese",
    "ban": "balinese",
    "bjn": "banjarese",
    "bug": "buginese",
    "ind": "indonesian",
    "jav": "javanese",
    "mad": "madurese",
    "min": "minangkabau",
    "nij": "ngaju",
    "sun": "sundanese",
    "bbc": "toba_batak",
}


class NusaXMT(datasets.GeneratorBasedBuilder):
    """NusaX-MT is a parallel corpus for training and benchmarking machine translation models across 10 Indonesian local languages + Indonesian and English. The data is presented in csv format with 12 columns, one column for each language."""

    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name=f"{lang1}-{lang2}", version=_SOURCE_VERSION)
        for lang1 in LANGUAGES_MAP
        for lang2 in LANGUAGES_MAP
        if lang1 != lang2
    ] + [
        datasets.BuilderConfig(name=f"ALL", version=_SOURCE_VERSION),
        datasets.BuilderConfig(name=f"BASELINE", version=_SOURCE_VERSION),
    ]

    DEFAULT_CONFIG_NAME = "ALL"

    def _info(self) -> datasets.DatasetInfo:
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "text_1": datasets.Value("string"),
                "text_2": datasets.Value("string"),
                "text_1_lang": datasets.Value("string"),
                "text_2_lang": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=features,
            homepage=_HOMEPAGE,
            license=_LICENSE,
            citation=_CITATION,
        )

    def _split_generators(
        self, dl_manager: datasets.DownloadManager
    ) -> List[datasets.SplitGenerator]:
        """Returns SplitGenerators."""
        train_csv_path = Path(dl_manager.download_and_extract(_URLS["train"]))
        validation_csv_path = Path(dl_manager.download_and_extract(_URLS["validation"]))
        test_csv_path = Path(dl_manager.download_and_extract(_URLS["test"]))

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={"filepath": train_csv_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"filepath": validation_csv_path},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={"filepath": test_csv_path},
            ),
        ]

    def _generate_examples(self, filepath: Path) -> Tuple[int, Dict]:
        df = pd.read_csv(filepath).reset_index()
        if self.config.name == "ALL":
            # load all 132 language pairs
            id_count = -1
            for lang_source in LANGUAGES_MAP:
                for lang_target in LANGUAGES_MAP:
                    if lang_source == lang_target:
                        continue

                    for _, row in df.iterrows():
                        id_count += 1
                        ex = {
                            "id": str(id_count),
                            "text_1": row[LANGUAGES_MAP[lang_source]],
                            "text_2": row[LANGUAGES_MAP[lang_target]],
                            "text_1_lang": lang_source,
                            "text_2_lang": lang_target,
                        }
                        yield id_count, ex

        elif self.config.name == "BASELINE":
            # load all 42 language pairs
            id_count = -1
            for lang_source in LANGUAGES_MAP:
                for lang_target in LANGUAGES_MAP:
                    if (
                        lang_source == lang_target
                        or lang_source not in _BASELINE_LANGUAGES
                        or lang_target not in _BASELINE_LANGUAGES
                    ):
                        continue

                    for _, row in df.iterrows():
                        id_count += 1
                        ex = {
                            "id": str(id_count),
                            "text_1": row[LANGUAGES_MAP[lang_source]],
                            "text_2": row[LANGUAGES_MAP[lang_target]],
                            "text_1_lang": lang_source,
                            "text_2_lang": lang_target,
                        }
                        yield id_count, ex

        else:
            df = pd.read_csv(filepath).reset_index()
            lang_source = self.config.name[0:3]
            lang_target = self.config.name[4:7]

            for index, row in df.iterrows():
                ex = {
                    "id": str(index),
                    "text_1": row[LANGUAGES_MAP[lang_source]],
                    "text_2": row[LANGUAGES_MAP[lang_target]],
                    "text_1_lang": lang_source,
                    "text_2_lang": lang_target,
                }
                yield str(index), ex
