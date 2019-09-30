from __future__ import division, absolute_import, print_function
from tqdm import tqdm
import re


def fetch_seq_info(dirname):
    '''
    Extract sequencing batch information from input directory filename

    Parameters
    ----------
    dirname : str
        Directory filename to parse
    '''
    # check directory path matches expected regex for raw sequencing data
    # matches YYMMDD_InstrumentSerialNumber_RunNumber_(A|B)FlowcellID
    pattern = re.compile(
        '^([0-9]{2})(0?[1-9]|1[012])(0[1-9]|[12]\\d|3[01])_(\\w{6})_(\\d{4})_(A|B)(\\w{9})/?$'
    )
    pass


def organize(dir, outdir=None, seqtype='mix'):
    '''
    Organize raw sequencing data folder

    Parameters
    ----------
    dir : str
        Input directory to organize
    outdir : str
        New path for input directory
    seqtype : str
        Type of sequencing data contained in the input folder.
        Must be one of ['atac', 'dname', 'chip', 'dna', 'rna', 'hic', 'mix'].
    '''
    pass
