# Utility Scripts

## Bible Scraper

To scrape a single translation of the Bible found in [Alkitab Mobi](https://alkitab.mobi/), run:

```sh
python utils/scrape.py --code {CODE} --outdir {OUTDIR}
```

For example, to download the Indonesian TB translation:

```sh
python utils/scrape.py --code tb --outdir corpus/
```

**Warning**: The webpage for Aralle Tabulahan translation of [Revelations 10](https://alkitab.mobi/aralle/Why/10/) is currently incorrect. Scraping `aralle` will lead to an error. 

### Parallel Scraping

To run scraping in parallel, run:

```sh
python utils/scrape_parallel.py \
    --codes {CODE} {CODE} \
    --outdir {OUTDIR} \
    -j {NUM_PROC}
```

For example, to download Indonesian and regional language translations with 4 processes, run

```sh
python utils/scrape_parallel.py \
    --codes abun aceh ambdr balantak bali bambam bauzi berik bugis dairi duri ende galela gorontalo iban jawa kaili_daa karo kupang lampung madura makasar mamasa manggarai mentawai meyah minang mongondow napu ngaju nias rote sabu sangir sasak simalungun sunda taa tabaru tb toba toraja uma yali yawa \
    --outdir corpus \
    -j 4
```

## Verse Aligner

To align a single corpus, run:

```sh
python utils/align.py --path {PATH_TO_JSON} --outdir {OUTDIR}
```

For example, to align the Indonesian TB translation:

```sh
python utils/align.py --path corpus/tb.json --outdir corpus_aligned
```