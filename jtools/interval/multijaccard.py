import numpy as np
import pandas as pd
import pybedtools as pbt
import matplotlib
# handle matplot lib backend nonsense
matplotlib.use('agg')
import matplotlib.pyplot
import seaborn as sns
from tqdm import tqdm

def multijaccard(bed, prefix='jaccard'):
    """
    Run bedtools jaccard for pairs of samples and plot as heatmap

    Parameters
    ==========
    bed : list<str>
        BED file paths
    prefix : str
        Prefix for output files
    """
    # placeholder for resultant data
    results = pd.DataFrame(columns=[
        'Index 1', 'Index 2', 'Sample 1', 'Sample 2', 'intersection',
        'union-intersection', 'jaccard', 'n_intersections'])
    for i, a in tqdm(enumerate(bed)):
        # initialize res dictionary
        res = {'Sample 1': a, 'Index 1': int(i)}
        bedA = pbt.BedTool(a)
        for j, b in tqdm(enumerate(bed[i:])):
            bedB = pbt.BedTool(b)
            # add second sample file
            res['Sample 2'] = b
            res['Index 2'] = int(i + j)
            # add dictionary result from bedtools jaccard to res
            res.update(bedA.jaccard(bedB))
            # append this as a new record in the DataFrame
            results.loc[len(results)] = res
    # save output table
    results.to_csv(prefix + '.tsv', sep='\t', index=False)
    # pivot for heatmap
    jaccard = results.pivot('Index 2', 'Index 1', 'jaccard')
    # mask for clean plotting
    mask = np.zeros_like(jaccard)
    mask[np.triu_indices_from(mask, 1)] = True
    g = sns.heatmap(jaccard, annot=True, fmt='.2f', mask=mask,
                    square=True, annot_kws={"size": 8})
    g.get_figure().savefig(prefix + '.pdf', figsize=(2 * len(bed)))
