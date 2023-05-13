# Machine Translation

## Indo-mT5

Indo-mT5 is mT5 fine-tuned for machine translation of regional languages of Indonesia. We release our dataset creation scripts, training code, and fine-tuned models for other to leverage.

There are two types of models:

- **Multilingual**: Many-to-many, multilingual translation model.
- **Bilingual**: Unidirectional, bilingual translation model.

We also further experiment with two settings:

- **Baseline**: Model trained on 7 languages (`ace`, `ban`, `bug`, `ind`, `jav`, `min`, `sun`).
- **All**: Model trained on 45 languages as listed [here](languages.md).

## Training

Our experiments are conducted in these steps:

- **Multilingual Training on Bible**: We first fine-tuned mT5 on multilingual translation on parallel Bible dataset, creating Indo-mT5.
- **Multilingual Training on NusaX**: We take Indo-mT5 and fine-tune them on multilingual pairs of the NusaX dataset.
- **Bilingual Training on NusaX**: We take Indo-mT5 and fine-tune them on bilingual pairs of the NusaX dataset.

Therefore, we have six training scripts:

| Dataset | Config   | Type         | Training Script                                                              | Evaluation Script                                                          |
| ------- | -------- | ------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Bible   | Baseline | Multilingual | [train_bible_baseline.sh](train_bible_baseline.sh)                           | [eval_bible_baseline.sh](eval_bible_baseline.sh)                           |
| Bible   | All (v2) | Multilingual | [train_bible_all.sh](train_bible_all.sh)                                     | [eval_bible_all.sh](eval_bible_all.sh)                                     |
| NusaX   | Baseline | Multilingual | [train_nusax_baseline_multilingual.sh](train_nusax_baseline_multilingual.sh) | [eval_nusax_baseline_multilingual.sh](eval_nusax_baseline_multilingual.sh) |
| NusaX   | All (v2) | Multilingual | [train_nusax_all_multilingual.sh](train_nusax_all_multilingual.sh)           | [eval_nusax_all_multilingual.sh](eval_nusax_all_multilingual.sh)           |
| NusaX   | Baseline | Bilingual    | [train_nusax_baseline_bilingual.sh](train_nusax_baseline_bilingual.sh)       | [eval_nusax_baseline_bilingual.sh](eval_nusax_baseline_bilingual.sh)       |
| NusaX   | All (v2) | Bilingual    | [train_nusax_all_bilingual.sh](train_nusax_all_bilingual.sh)                 | [eval_nusax_all_bilingual.sh](eval_nusax_all_bilingual.sh)                 |

## Results

We evaluated our models on NusaX (Winata et al., 2022) and compared them to existing models.

### `ind -> x`

| Model                                | #params |   `ace`   |   `ban`   |   `bbc`   |   `bjn`   |   `bug`   |   `jav`   |   `mad`   |   `min`   |   `nij`   |   `sun`   |    avg    |
| ------------------------------------ | ------- | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| IndoGPT (Winata et al., 2022)        | 117M    |   9.60    |   14.17   |   8.20    |   22.23   |   5.18    |   24.05   |   14.44   |   26.95   |   17.56   |   23.15   |   16.55   |
| IndoBART v2 (Winata et al., 2022)    | 132M    | **19.21** | **27.08** | **18.41** | **40.03** | **11.06** | **39.97** |   28.95   |   48.48   | **27.11** | **38.46** |   29.88   |
| mBART-50 Large (Winata et al., 2022) | 610M    |   17.21   |   22.67   |   17.79   |   34.26   |   10.78   |   35.33   |   28.63   |   43.87   |   25.91   |   31.21   |   26.77   |
| mT5 Base (Winata et al., 2022)       | 580M    |   14.79   |   18.07   |   18.22   |   38.64   |   6.68    |   33.48   |   0.96    |   45.84   |   13.59   |   33.79   |   22.41   |
| NLLB-200 Distilled (zero-shot)       | 600M    |   2.74    |   4.87    |     -     |     -     |   1.66    |   17.66   |     -     |   9.79    |     -     |   11.92   |   8.11    |
| Indo-mT5 NusaX Multilingual          | 580M    |   16.02   |   22.48   |     -     |     -     |   8.86    |   33.65   |     -     |   33.65   |     -     |   29.76   |   24.07   |
| Indo-mT5 NusaX Bilingual             | 580M    |   17.99   |   27.03   |     -     |     -     |   10.80   |   39.63   |     -     | **51.56** |     -     |   35.16   | **30.36** |
| Indo-mT5 v2 NusaX Multilingual       | 580M    |   14.28   |   19.19   |   14.86   |   28.39   |   8.05    |   28.70   |   20.95   |   32.70   |   22.30   |   26.19   |   21.56   |
| Indo-mT5 v2 NusaX Bilingual          | 580M    |   17.58   |   24.24   |   16.69   |   38.81   |   10.20   |   37.87   | **29.77** |   50.90   |   26.93   |   34.22   |   28.72   |

### `x -> ind`

| Model                                | #params |   `ace`   |   `ban`   |   `bbc`   |   `bjn`   |   `bug`   |   `jav`   |   `mad`   |   `min`   |   `nij`   |   `sun`   |    avg    |
| ------------------------------------ | ------- | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: | :-------: |
| IndoGPT (Winata et al., 2022)        | 117M    |   7.01    |   13.23   |   5.27    |   19.53   |   1.98    |   27.31   |   13.75   |   23.03   |   10.83   |   23.18   |   14.51   |
| IndoBART v2 (Winata et al., 2022)    | 132M    |   24.44   |   40.49   |   19.94   | **47.81** |   12.64   | **50.64** |   36.10   |   58.38   | **33.50** | **45.96** |   36.99   |
| mBART-50 Large (Winata et al., 2022) | 610M    |   18.45   |   34.23   |   17.43   |   41.73   |   10.87   |   39.66   |   32.11   |   59.66   |   29.84   |   35.19   |   31.92   |
| mT5 Base (Winata et al., 2022)       | 580M    |   18.59   |   21.73   |   12.85   |   42.29   |   2.64    |   45.22   |   32.35   |   58.65   |   25.61   |   36.58   |   29.65   |
| NLLB-200 Distilled (zero-shot)       | 600M    |   9.42    |   21.24   |     -     |     -     |   6.18    |   30.54   |     -     |   40.49   |     -     |   26.91   |   22.46   |
| Indo-mT5 NusaX Multilingual          | 580M    |   23.94   |   35.30   |     -     |     -     | **16.68** |   29.76   |     -     |   48.10   |     -     |   36.54   |   31.72   |
| Indo-mT5 NusaX Bilingual             | 580M    | **24.78** | **42.15** |     -     |     -     |   16.27   |   47.26   |     -     | **62.94** |     -     |   42.39   | **39.30** |
| Indo-mT5 v2 NusaX Multilingual       | 580M    |   21.01   |   30.43   |   18.57   |   34.21   |   14.42   |   35.19   |   27.04   |   42.64   |   26.90   |   33.78   |   28.42   |
| Indo-mT5 v2 NusaX Bilingual          | 580M    |   22.87   |   39.48   | **20.48** |   44.53   |   15.97   |   45.20   | **36.65** |   60.97   |   32.38   |   39.80   |   35.83   |

## Parallel Bible Dataset Creation

This will cover the creation process of our Bible machine-translation dataset.

### Overview

1. Scrape Bible Data
2. Align Bible Verses
3. Load as Machine-Translation Dataset

### Bible Scraping

```sh
python utils/scrape_parallel.py \
    --codes abun aceh ambdr aralle balantak bali bambam bauzi berik bugis dairi duri ende galela gorontalo iban jawa kaili_daa karo kupang lampung madura makasar mamasa manggarai mentawai meyah minang mongondow napu ngaju nias rote sabu sangir sasak simalungun sunda taa tabaru tb toba toraja uma yali yawa \
    --outdir corpus \
    -j 4
```

### Align Bible Verses

```sh
for LANGUAGE in abun aceh ambdr aralle balantak bali bambam bauzi berik bugis dairi duri ende galela gorontalo iban jawa kaili_daa karo kupang lampung madura makasar mamasa manggarai mentawai meyah minang mongondow napu ngaju nias rote sabu sangir sasak simalungun sunda taa tabaru tb toba toraja uma yali yawa
do
    python utils/align.py --path corpus/$LANGUAGE.json --outdir corpus_aligned
done
```

You can read more about aligning Bible verses in [our blogpost](https://lazarusnlp.github.io/blogs/bible_alignment/).

### Data Loading Script

In the data loading script, we have to do these two steps:

1. Split unique verse IDs into train/test/validation subsets.
2. Generate permutations of every verse ID for every subset.

You can find our data loading implementation in [src/alkitab-sabda-mt.py](src/alkitab-sabda-mt.py).