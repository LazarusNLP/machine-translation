from argparse import ArgumentParser
from multiprocessing import Pool, RLock

from tqdm.auto import tqdm
from scrape import BibleScraper

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--codes",
        type=str,
        nargs="+",
        required=True,
        help="Bible language code in Alkitab Mobi",
    )
    parser.add_argument(
        "--outdir", type=str, required=True, help="Path to output directory"
    )
    parser.add_argument(
        "-j",
        type=int,
        default=1,
        help="Number of parallel processes. Specify `j=0` to use all available processes as provided by `os.cpu_count()`",
    )
    args = parser.parse_args()

    processes = args.j if args.j > 0 else None
    pool = Pool(processes=processes, initargs=(RLock(),), initializer=tqdm.set_lock)
    args_list = [(code, args.outdir) for code in args.codes]
    jobs = [
        pool.apply_async(
            BibleScraper.scrape,
            args=(
                code,
                outdir,
                pid,
            ),
        )
        for pid, (code, outdir) in enumerate(args_list)
    ]
    pool.close()
    result_list = [job.get() for job in jobs]
