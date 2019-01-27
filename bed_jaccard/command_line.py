import os.path
import argparse
from . import run


def main():
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    PARSER.add_argument(
        "bed",
        type=str,
        help="BED file(s)",
        nargs='+'
    )
    PARSER.add_argument(
        "-o", "--prefix",
        type=str,
        help="Prefix for output files.",
        default='jaccard'
    )
    ARGS = PARSER.parse_args()
    nonex_files = [b for b in ARGS.bed if not os.path.exists(b)]
    if len(nonex_files) != 0:
        raise OSError(' '.join([nonex_files[0], 'not found.']))
    run(ARGS.bed, ARGS.prefix)
