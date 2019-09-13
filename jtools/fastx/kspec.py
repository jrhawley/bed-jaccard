import pysam

from ..utils import detect_filetype_from_path

def get_kmers(s, k):
    '''
    Get all k-mers from the sequence

    Parameters
    ----------
    s : str
        Sequence to parse
    k : int
        size of the k-mer
    '''
    return [s[i:(i + k)] for i in range(0, len(s) - k + 1)]

def minimal_lmer(kmer, l):
    '''
    Get the minimal l-mer of a given k-mer 

    Parameters
    ----------
    kmer : str
        k-mer to parse
    l : int
        size of l-mer
    
    '''
    return min(get_kmers(kmer, l))
    

def kspec(fastxfile, k):
    # l for minimal l-mer sorting
    l = k // 3
    # minimal l-mer for fast access to k-mer counts
    min_l = {}
    # kmer counts
    kmer_counts = {}
    kmer_possible = 4^k
    fx = pysam.FastxFile(fastxfile)
    # start reading sequences
    read = next(fx)
    prev_min_lmer = minimal_lmer(kmer, l)
    for kmer in get_kmers(read.sequence, k):
                
