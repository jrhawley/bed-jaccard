import os.path as path
import argparse

def validate_multijaccard(ARGS):
    '''
    Validate command line arguments for multijaccard

    Parameters
    ----------
    ARGS : Namespace
        Command line arguments
    '''
    nonex_files = [b for b in ARGS.bed if not path.exists(b)]
    if len(nonex_files) != 0:
        raise OSError(' '.join([nonex_files[0], 'not found.']))

    

def main():
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    SUBPARSERS = PARSER.add_subparsers(
        title='Sub-commands', dest='command', metavar='<command>')
    
    # multi-jaccard
    multijaccard_parser = SUBPARSERS.add_parser(
        'multi-jaccard',
        help='Perform `bedtools jaccard` on multiple BED files, and cluster samples by their pair-wise Jaccard indices.'
    )
    multijaccard_parser.add_argument(
        'bed',
        type=str,
        help="BED file(s)",
        nargs='+'
    )
    multijaccard_parser.add_argument(
        '-o', '--prefix',
        type=str,
        help='Prefix for output files.',
        default='jaccard'
    )

    # parse arguments from command line
    ARGS = PARSER.parse_args()

    # validate command line arguments for the give sub-command
    # import packages after parsing to speed up command line responsiveness
    if ARGS.command == 'multi-jaccard':
        validate_multijaccard(ARGS)
        from .interval.multijaccard import multijaccard
        multijaccard(ARGS.bed, ARGS.prefix)
    else:
        pass
