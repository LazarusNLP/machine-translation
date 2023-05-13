import json
from pathlib import Path
from itertools import permutations
from typing import Dict, List, Tuple

import datasets
from sklearn.model_selection import train_test_split

_SOURCE_VERSION = "1.0.0"
_CITATION = ""
_DESCRIPTION = ""
_HOMEPAGE = ""
_LICENSE = ""
_CORPUS_DIR = "corpus_aligned"
_CORPUS_URL = "https://huggingface.co/datasets/LazarusNLP/alkitab-sabda-mt/resolve/main/corpus_aligned.tar.gz"

BIBLE2ISO = {
    "abun": "kgr",
    "aceh": "ace",
    "ambdr": "abs",
    "aralle": "atq",
    "balantak": "blz",
    "bali": "ban",
    "bambam": "ptu",
    "bauzi": "bvz",
    "berik": "bkl",
    "bugis": "bug",
    "dairi": "btd",
    "duri": "mvp",
    "ende": "end",
    "galela": "gbi",
    "gorontalo": "gor",
    "iban": "iba",
    "jawa": "jav",
    "kaili_daa": "kzf",
    "karo": "btx",
    "kupang": "mkn",
    "lampung": "ljp",
    "madura": "mad",
    "makasar": "mak",
    "mamasa": "mqj",
    "manggarai": "mqy",
    "mentawai": "mwv",
    "meyah": "mej",
    "minang": "min",
    "mongondow": "mog",
    "napu": "npy",
    "ngaju": "nij",
    "nias": "nia",
    "rote": "twu",
    "sabu": "hvn",
    "sangir": "sxn",
    "sasak": "sas",
    "simalungun": "bts",
    "sunda": "sun",
    "taa": "pmf",
    "tabaru": "tby",
    "tb": "ind",
    "toba": "bbc",
    "toraja": "sda",
    "uma": "ppk",
    "yali": "yli",
    "yawa": "yva",
}

_LANGUAGES = sorted(list(BIBLE2ISO.values()))
_BASELINE_LANGUAGES = ["ace", "ban", "bug", "ind", "jav", "min", "sun"]

# _FILES = {lang: f"{_CORPUS_DIR}/{lang}.json" for lang in BIBLE2ISO}


class AlkitabSabdaMT(datasets.GeneratorBasedBuilder):
    BUILDER_CONFIGS = [
        datasets.BuilderConfig(name="all", version=_SOURCE_VERSION),
        datasets.BuilderConfig(name="baseline", version=_SOURCE_VERSION),
    ] + [
        datasets.BuilderConfig(name=f"{lang1}-{lang2}", version=_SOURCE_VERSION)
        for lang1, lang2 in permutations(_LANGUAGES, 2)
    ]

    DEFAULT_CONFIG_NAME = "all"

    def _info(self) -> datasets.DatasetInfo:
        features = datasets.Features(
            {
                "verse_id": datasets.Value("string"),
                "lang_source": datasets.Value("string"),
                "lang_target": datasets.Value("string"),
                "text_source": datasets.Value("string"),
                "text_target": datasets.Value("string"),
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

        def create_queryable_corpus(corpus: List[Dict]) -> Dict[str, str]:
            return {datum["verse_id"]: datum["text"] for datum in corpus}

        extracted_path = (
            Path(dl_manager.download_and_extract(_CORPUS_URL)) / _CORPUS_DIR
        )
        corpus = {
            BIBLE2ISO[lang]: json.load(
                open((extracted_path / lang).with_suffix(".json"))
            )
            for lang in BIBLE2ISO
        }

        queryable_corpus = {
            lang: create_queryable_corpus(corpora) for lang, corpora in corpus.items()
        }

        verse_ids = sorted(
            set([verse["verse_id"] for corpora in corpus.values() for verse in corpora])
        )

        train_val_ids, test_ids = train_test_split(
            verse_ids, test_size=0.2, random_state=41
        )
        train_ids, val_ids = train_test_split(
            train_val_ids, test_size=0.125, random_state=41
        )

        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                gen_kwargs={
                    "queryable_corpus": queryable_corpus,
                    "verse_ids": train_ids,
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                gen_kwargs={"queryable_corpus": queryable_corpus, "verse_ids": val_ids},
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                gen_kwargs={
                    "queryable_corpus": queryable_corpus,
                    "verse_ids": test_ids,
                },
            ),
        ]

    def _generate_examples(
        self, queryable_corpus: Dict[str, str], verse_ids: List[str]
    ) -> Tuple[int, Dict]:
        if self.config.name == "all":
            language_pairs = list(permutations(_LANGUAGES, 2))
        elif self.config.name == "baseline":
            language_pairs = list(permutations(_BASELINE_LANGUAGES, 2))
        else:
            language_pairs = tuple([self.config.name.split("-")])

        idx = -1
        for verse_id in verse_ids:
            # generate all permutation pairs of that verse id
            for source, target in language_pairs:
                source_corpus = queryable_corpus[source]
                target_corpus = queryable_corpus[target]

                if verse_id in source_corpus and verse_id in target_corpus:
                    idx += 1
                    datum = {
                        "verse_id": verse_id,
                        "lang_source": source,
                        "lang_target": target,
                        "text_source": source_corpus[verse_id],
                        "text_target": target_corpus[verse_id],
                    }
                    yield idx, datum
