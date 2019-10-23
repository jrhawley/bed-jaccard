from Bio import SeqIO
from gzip import open as gzopen

def fastq_to_fasta(fq, fa):
    '''
    Convert FASTQ file to FASTA format

    Parameters
    ----------
    fq : str
        Input FASTQ file
    fa : str
        Output FASTA file
    '''
    # check for file format
    if fq.endswith('.gz'):
        fq_handle = gzopen(fq, 'rt')
    else:
        fq_handle = open(fq, 'r')
    if fa.endswith('.gz'):
        fa_handle = gzopen(fa, 'wt')
    else:
        fa_handle = open(fa, 'w')
    # load reads for random access
    records = SeqIO.parse(fq_handle, 'fastq')
    # load `chunksize` reads at a time
    chunked_records = grouper(records, chunksize)
    for chunk in chunked_records:
        # filter chunk
        chunk = [r for r in chunk if r is not None]
        fa_handle.write(chunk)
    fq_handle.close()
    fa_handle.close()
