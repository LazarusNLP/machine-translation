import json
import os
import re
from argparse import ArgumentParser
from typing import Dict, List, Tuple
from urllib import request

from bs4 import BeautifulSoup
from tqdm.auto import tqdm


class BibleScraper:
    # https://ubsicap.github.io/usfm/identification/books.html
    BOOK2USFM = {
        "Kej": "GEN",
        "Kel": "EXO",
        "Ima": "LEV",
        "Bil": "NUM",
        "Ula": "DEU",
        "Yos": "JOS",
        "Hak": "JDG",
        "Rut": "RUT",
        "1Sa": "1SA",
        "2Sa": "2SA",
        "1Ra": "1KI",
        "2Ra": "2KI",
        "1Ta": "1CH",
        "2Ta": "2CH",
        "Ezr": "EZR",
        "Neh": "NEH",
        "Est": "EST",
        "Ayb": "JOB",
        "Mzm": "PSA",
        "Ams": "PRO",
        "Pkh": "ECC",
        "Kid": "SNG",
        "Yes": "ISA",
        "Yer": "JER",
        "Rat": "LAM",
        "Yeh": "EZK",
        "Dan": "DAN",
        "Hos": "HOS",
        "Yoe": "JOL",
        "Amo": "AMO",
        "Oba": "OBA",
        "Yun": "JON",
        "Mik": "MIC",
        "Nah": "NAM",
        "Hab": "HAB",
        "Zef": "ZEP",
        "Hag": "HAG",
        "Zak": "ZEC",
        "Mal": "MAL",
        "Mat": "MAT",
        "Mrk": "MRK",
        "Luk": "LUK",
        "Yoh": "JHN",
        "Kis": "ACT",
        "Rom": "ROM",
        "1Ko": "1CO",
        "2Ko": "2CO",
        "Gal": "GAL",
        "Efe": "EPH",
        "Flp": "PHP",
        "Kol": "COL",
        "1Te": "1TH",
        "2Te": "2TH",
        "1Ti": "1TI",
        "2Ti": "2TI",
        "Tit": "TIT",
        "Flm": "PHM",
        "Ibr": "HEB",
        "Yak": "JAB",
        "1Pt": "1PE",
        "2Pt": "2PE",
        "1Yo": "1JN",
        "2Yo": "2JN",
        "3Yo": "3JN",
        "Yud": "JUD",
        "Why": "REV",
    }

    @staticmethod
    def postprocess(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

    @staticmethod
    def parse_verse_line(line: str) -> Tuple[str, str]:
        verse_number, text = None, ""
        contents = line.contents

        # incomplete verse (e.g. Genesis 35:22b TB)
        if len(contents) == 1:
            # ignore pericopes
            if contents[0].name != "span":
                text = contents[0]

        elif len(contents) >= 2:
            verse_number = contents[0].text
            for content in contents[1:]:
                text += content.text

        return (verse_number, BibleScraper.postprocess(text))

    @staticmethod
    def scrape_chapter(chapter_url: str) -> List[Tuple[str, str]]:
        chapter_soup = BeautifulSoup(request.urlopen(chapter_url), features="lxml")
        divs = chapter_soup.find_all("div")
        try:
            _ = divs[2]["class"][0]
            # contains audio player
            lines = divs[4].find_all("p")
        except:
            lines = divs[2].find_all("p")

        try:
            return [BibleScraper.parse_verse_line(line) for line in lines]
        except Exception as exc:
            print(f"Errored at {chapter_url}")
            raise exc

    @staticmethod
    def scrape(code: str, outdir: str, pid=0) -> List[Dict[str, str]]:
        url = f"https://alkitab.mobi/{code}/"
        save_name = f"{outdir}/{code}.json"

        if os.path.exists(save_name):
            print(f"{code} already scraped, skipping.")
            return

        bible_soup = BeautifulSoup(request.urlopen(url), features="lxml")
        testaments = bible_soup.find_all("span", {"class": "style0"})
        books = [
            book.get("href")
            for testament in testaments
            for book in testament.find_all("a")
        ]
        data = []

        for book_url in tqdm(books, desc=code, position=pid + 1):
            book_name = book_url.split("/")[-2]
            book_soup = BeautifulSoup(request.urlopen(book_url), features="lxml")
            chapters = [
                chapter.get("href")
                for chapter in book_soup.find("span", {"class": "style2"}).find_all("a")
            ]
            for chapter_url in chapters:
                chapter_number = chapter_url.split("/")[-2]
                for (verse_num, text) in BibleScraper.scrape_chapter(chapter_url):
                    if text != "":
                        data.append(
                            {
                                "url": chapter_url,
                                "book_id": BibleScraper.BOOK2USFM[book_name],
                                "book": book_name,
                                "chapter": chapter_number,
                                "verse": verse_num,
                                "text": text,
                            }
                        )

        with open(save_name, "w") as fp:
            json.dump(data, fp, indent=4)

        return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--code", type=str, required=True, help="Bible language code in Alkitab Mobi"
    )
    parser.add_argument(
        "--outdir", type=str, required=True, help="Path to output directory"
    )
    args = parser.parse_args()
    BibleScraper.scrape(code=args.code, outdir=args.outdir)
