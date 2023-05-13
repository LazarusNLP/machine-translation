from argparse import ArgumentParser
from typing import List, Dict
import json
import re


class Aligner:
    @staticmethod
    def postprocess(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

    @staticmethod
    def remove_verse_ids(text: str) -> str:
        matches = re.findall("\(\d+.*?\)", text)
        for match in matches:
            text = text.replace(match, "")
        return Aligner.postprocess(text)

    @staticmethod
    def align(json_path: str, outdir: str) -> List[Dict[str, str]]:
        data = json.load(open(json_path))
        save_name = f"{outdir}/{json_path.split('/')[-1]}"

        for idx, datum in enumerate(data):
            # get incomplete verses, marked by empty `verse`
            if datum["verse"] == None:
                # get parent verse
                parent_verse = data[idx - 1]
                # append incomplete verse to parent verse
                parent_verse["text"] = parent_verse["text"] + " " + datum["text"]

        # drop incomplete verses
        data = [datum for datum in data if datum["verse"] != None]

        # remove in-text verse ids
        for datum in data:
            datum["text"] = Aligner.remove_verse_ids(datum["text"])

        # align verse ranges
        count = 0
        for idx, datum in enumerate(data):
            # count how many empty, range-only verses
            if datum["text"] == "":
                count += 1
                continue
            else:
                parent_index = idx - count - 1
                # update parent verse once non-empty is found
                if count > 0:
                    # update parent verse
                    data[parent_index]["verse"] = (
                        data[parent_index]["verse"] + "-" + data[idx - 1]["verse"]
                    )
                    count = 0

        # drop empty verses
        data = [datum for datum in data if datum["text"] != ""]

        # {verse_id} = {book_id}_{chapter}_{verse}
        for datum in data:
            datum["verse_id"] = f'{datum["book_id"]}_{datum["chapter"]}_{datum["verse"]}'

        with open(save_name, "w") as fp:
            json.dump(data, fp, indent=4)

        return data


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--path", type=str, required=True, help="Path to scraped corpus"
    )
    parser.add_argument(
        "--outdir", type=str, required=True, help="Path to output directory"
    )
    args = parser.parse_args()
    Aligner.align(json_path=args.path, outdir=args.outdir)
