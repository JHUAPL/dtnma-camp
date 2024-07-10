''' Shared test fixture utilities.
'''
import argparse
import os

from camp.tools.camp import run

# This util file should be in the same directory as the
# anms-adms and dtnma-tools repos
_util_path = os.path.dirname(os.path.abspath(__file__))
ADMS_DIR = os.path.join(_util_path, "anms-adms")
DTNMA_TOOLS_DIR = os.path.join(_util_path, "dtnma-tools")

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
