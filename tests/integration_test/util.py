''' Shared test fixture utilities.
'''
import argparse

from camp.tools.camp import run

def _run_camp(filepath, outpath, only_sql, only_ch, scrape=False):
    """
    Generates sql files by running CAmp on filepath. Resulting sql files are stored
    in outpath. 
    """
    args = argparse.Namespace()
    args.admfile = filepath
    args.out = outpath
    args.only_sql = only_sql
    args.only_ch = only_ch
    args.scrape = scrape
    return run(args)
