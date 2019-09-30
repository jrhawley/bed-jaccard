from __future__ import division, absolute_import, print_function
import re
from datetime import datetime
from os import listdir, mkdir, rename
import os.path as path
from . import *


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
    # see https://www.biostars.org/p/124972/, https://www.biostars.org/p/198143/
    pattern = re.compile(DIRNAME_REGEX)
    m = re.match(pattern, dirname)
    vals = {
        'date': datetime.strptime(''.join([m.group(1), m.group(2), m.group(3)]), '%y%m%d'),
        'instrument': m.group(4),
        'run': m.group(5),
        'position': m.group(6),
        'flowcell': m.group(7),
        'date_sub': '',
        'description': ''
    }
    vals['date_rec'] = vals['date'].strftime('%Y-%m-%d')
    return vals


def create_cluster_params(outfile):
    '''
    Create `cluster.yaml` file

    Parameters
    ----------
    outfile : str
        Output config file to create
    '''
    fh = open(outfile, 'w')
    fh.write(CLUSTER_STR)
    fh.close()


def create_readme(seq_info, outfile):
    '''
    Create `README.md` file

    Parameters
    ----------
    seq_info : Dict of {str, Object}
        Sequencing metadata retrieved from directory name
    outfile : str
        Output config file to create
    '''
    fh = open(outfile, 'w')
    fh.write(README_STR.format(**seq_info))
    fh.close()


def create_config(fastq_dir, outfile):
    '''
    Create `config.tsv` file

    Parameters
    ----------
    fastq_dir : str
        Directory containing FASTQs files to parse
    outfile : str
        Output config file to create
    '''
    pass


def create_snakefile(seqtype='mix', outfile):
    '''
    Create `Snakefile` config file

    Parameters
    ----------
    seqtype : str
        Type of sequencing data contained in the input folder.
        Must be one of ['atac', 'dname', 'chip', 'dna', 'rna', 'hic', 'mix'].
    outfile : str
        Output config file to create
    '''
    pass


def organize(indir, outdir=None, seqtype='mix'):
    '''
    Organize raw sequencing data folder

    Parameters
    ----------
    indir : str
        Input directory to organize
    outdir : str
        New path for input directory
    seqtype : str
        Type of sequencing data contained in the input folder.
        Must be one of ['atac', 'dname', 'chip', 'dna', 'rna', 'hic', 'mix'].
    '''
    # extract sequencing metadata information from directory name
    seq_info = fetch_seq_info(indir)
    default_dirs = RESERVED_DIRS
    if seqtype == 'atac' or seqtype == 'chip':
        default_dirs += ['Peaks']
    elif seqtype == 'dname':
        default_dirs += ['Methylation']
    elif seqtype == 'hic':
        default_dirs += ['Contacts']
    # make directories
    for d in default_dirs:
        dir_to_make = path.join(indir, d)
        if not path.exists(dir_to_make):
            mkdir(dir_to_make)
    # find FASTQs in directory
    dir_files = listdir(indir)
    fastq_files = [f for f in dir_files if f.endswith('.fastq.gz')]
    other_files = [f for f in dir_files if not f.endswith('.fastq.gz') and f not in RESERVED_FILENAMES]
    # move FASTQs into `FASTQs` directory
    for f in fastq_files:
        target = path.join(indir, f)
        dest = path.join(indir, 'FASTQs', f)
        rename(target, dest)
    for f in other_files:
        target = path.join(indir, f)
        dest = path.join(indir, 'Reports', f)
        if not path.isdir(target):
            rename(target, dest)
        else:
            if f not in RESERVED_DIRS:
                rename(target, dest)
    # check for README and other config files in directory
    reserved_files = [path.join(indir, f) for f in RESERVED_FILENAMES]
    if not path.exists(reserved_files[0]):
        create_readme(seq_info, reserved_files[0])
    if not path.exists(reserved_files[1]):
        create_cluster_params(reserved_files[1])
    # if not path.exists(reserved_files[2]):
    #     create_config(path.join(indir, RESERVED_DIRS[1]), reserved_files[3])
    # if not path.exists(reserved_files[3]):
    #     create_snakefile(seqtype, reserved_files[3])
    # rename directory if asked to
    if outdir is not None:
        rename(indir, outdir)
