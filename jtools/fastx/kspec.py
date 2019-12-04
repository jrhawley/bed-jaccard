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
    s = s.lower()
    return [s[i:(i + k)] for i in range(0, len(s) - k + 1)]


def minimal_kmer(s, k):
    '''
    Get the minimal k-mer of a given sequence 

    Parameters
    ----------
    s : str
        Sequence to parse
    k : int
        size of k-mer

    '''
    kmers = get_kmers(s, k)
    min_kmer = min(kmers)
    idx = kmers.index(min_kmer)
    return min_kmer, idx


def get_k_bookends(s, k):
    '''
    Get k-mers at beginning and end of a string

    Parameters
    ----------
    s : str
        Sequence to parse
    k : int
        Length of k-mer
    '''
    s = s.lower()
    return s[:k], s[-k:]


def kspec(fastxfile, k):
    '''
    Calculate the k-mer spectrum for a FASTX file

    Parameters
    ----------
    fastxfile : str
        FASTX file path
    k : int
        Length of k-mers to generate
    '''
    # l for minimal l-mer sorting for faster kmer indexing
    l = k // 3
    # kmer counts
    kmer_counts = {}
    fx = pysam.FastxFile(fastxfile)
    # start reading sequences
    read = next(fx)
    prev_min_lmer, prev_idx = minimal_kmer(read.sequence[:k], l)
    for i, kmer in enumerate(get_kmers(read.sequence, k)):
        if prev_idx < i:
            min_lmer, min_idx = minimal_kmer(kmer, l)
            # keep index global to the sequence, not the kmer
            min_idx = min_idx + i
        else:
            if prev_min_lmer > kmer[-l:]:
                min_lmer = kmer[-l:]
                min_idx = i + k - l
            else:
                min_lmer = prev_min_lmer
                min_idx = prev_idx
        if min_lmer not in kmer_counts:
            kmer_counts[min_lmer] = {kmer: 0}
        elif kmer not in kmer_counts[min_lmer]:
            kmer_counts[min_lmer][kmer] = 0
        # count kmer
        kmer_counts[min_lmer][kmer] += 1
        # update prev_ values for next comparison
        prev_min_lmer = min_lmer
        prev_idx = min_idx
    # flatten results to return all kmers
    return {key: val for d in kmer_counts for key, val in kmer_counts[d].items()}
