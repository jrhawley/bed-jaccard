
"""
bed-jaccard
==========

Simple, one-liner for calculating and visualizing Jaccard index for multiple samples
"""

from __future__ import division, absolute_import, print_function
import os.path
import argparse
import numpy as np
import pandas as pd
import pybedtools as pbt
import seaborn as sns
import matplotlib.pyplot as plt

plt.switch_backend('agg')


def main():
    """
    Main
    """
    # placeholder for resultant data
    results = pd.DataFrame(columns=[
        'Index 1', 'Index 2', 'Sample 1', 'Sample 2', 'intersection',
        'union-intersection', 'jaccard', 'n_intersections'])
    for i, a in enumerate(ARGS.bed):
        # initialize res dictionary
        res = {'Sample 1': a, 'Index 1': int(i)}
        bedA = pbt.BedTool(a)
        for j, b in enumerate(ARGS.bed[i:]):
            bedB = pbt.BedTool(b)
            # add second sample file
            res['Sample 2'] = b
            res['Index 2'] = int(i + j)
            # add dictionary result from bedtools jaccard to res
            res.update(bedA.jaccard(bedB))
            # append this as a new record in the DataFrame
            results.loc[len(results)] = res
    # save output table
    results.to_csv(ARGS.prefix + '.tsv', sep='\t', index=False)
    # pivot for heatmap
    jaccard = results.pivot('Index 2', 'Index 1', 'jaccard')
    # mask for clean plotting
    mask = np.zeros_like(jaccard)
    mask[np.triu_indices_from(mask, 1)] = True
    g = sns.heatmap(jaccard, annot=True, fmt='.2f', mask=mask,
                    square=True)
    g.get_figure().savefig(ARGS.prefix + '.pdf', figsize=(2 * len(ARGS.bed)))


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "bed",
        type=str,
        help="BED file(s)",
        nargs='+'
    )
    PARSER.add_argument(
        "-o", "--prefix",
        type=str,
        help="Prefix for output files",
        default='jaccard'
    )
    ARGS = PARSER.parse_args()
    nonex_files = [b for b in ARGS.bed if not os.path.exists(b)]
    if len(nonex_files) != 0:
        raise OSError(' '.join([nonex_files[0], 'not found.']))
    main()
