#! /usr/bin/python

"""A script for downloading fastq files concurrently.

This script aims to download fastq files concurrently. The SRA accession numbers are stored in different
csv files. The names of the csv files are the BioExperiment IDs.
"""
import os
import subprocess
from multiprocessing import Pool

# Path to the directory in which the fastq files are stored
DATA_PATH = "/home/mali/NewDrive/Project/FSL/Data"
def read_file(csv_path):
    """Reads in a csv file.

    Parameters
    ----------
    csv_path : str
        A str refers to a path to the csv file.

    Returns
    -------
    List
        A list contains the SRA accession numbers
    """
    with open(csv_path, "r") as file:
        tmp_list = file.read().replace("\n", "").split(",")
    return tmp_list

def dump_fastq(sra_number):
    """The function prefetches and dumps a sra file with the given sra_number

    Parameters
    ----------
    sra_number : str
        A string refers to a SRA accession number.
    """
    # mkdir_cmd = f"mkdir {sra_path}"
    # os.system(mkdir_cmd)
    prefetch_cmd = f"prefetch {sra_number} -O {DATA_PATH}"
    subprocess.call(prefetch_cmd)
    subprocess.call(f"echo {sra_number} prefetched")

    sra_path = os.path.join(DATA_PATH, sra_number)
    fasterq_dump_cmd = f"fasterq-dump {sra_path} -O {sra_path}"
    subprocess.call(fasterq_dump_cmd)

    fastq_path = os.path.join(sra_path, "*.fastq")
    gzip_cmd = f"gzip {fastq_path}"
    subprocess.call(gzip_cmd)

# sra_list = read_file("PRJEB40875.csv")
sra_list = read_file("PRJEB28329.csv")
print(f"{len(sra_list)} files are going to dump.")

with Pool(3) as pool:
    pool.map(dump_fastq, sra_list)