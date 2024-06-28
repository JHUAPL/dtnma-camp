import psycopg2
import unittest
import argparse
import os
import ace
import pytest

from .util import TmpDir
from camp.tools.camp import run

SELFDIR = os.path.dirname(__file__)
ADMS_DIR = os.path.join(SELFDIR, "adms")

# @pytest.fixture()
@pytest.fixture(scope="session", autouse=True)
def setup():
    # setup
    # connect to ANMS library
    conn = psycopg2.connect(
            host="172.17.0.4", # might need to change? or pass through somehow?
            port=5432,
            user="postgres",
            password="root"
    )
    cursor = conn.cursor()
    admset = ace.AdmSet()

    yield cursor, admset

    # teardown
    cursor.close()
    conn.close()

def _runCamp(filepath, outpath):
    """
    Generates sql files by running CAmp on filepath. Result sql files are stored
    in outpath
    """
    args = argparse.Namespace()
    args.admfile = filepath
    args.out = outpath
    args.only_sql = True
    args.only_ch = False
    return run(args)


# TODO which files to use? how many files? 1 file = 1 test case?
#      using existing file for now...
@pytest.mark.parametrize("adm", [f for f in os.listdir(ADMS_DIR) if os.path.isfile(os.path.join(ADMS_DIR, f))])
def test_adms(setup, adm):
    """
    Integration test for all an ADM found in the ADMS_DIR folder
    Resulting sql files will be placed in ADMS_DIR/amp-sql/Agent_Scripts
    """
    cursor = setup[0]
    admset = setup[1]

    # make sure file is .json or .yaml
    # and not the index.json file
    ext = os.path.splitext(adm)[1]
    if (ext != ".json" and ext != ".yaml") or adm == "index.json":
        pytest.skip("file skipped: {f} is not an adm file".format(f=adm))

    # run camp
    filepath = os.path.join(ADMS_DIR, adm)
    exitcode = _runCamp(filepath, ADMS_DIR)
    assert 0 == exitcode

    # execute sql
    norm_name = admset.load_from_file(filepath).norm_name
    sql_file = os.path.join(ADMS_DIR, "amp-sql", "Agent_Scripts", 'adm_{name}.sql'.format(name=norm_name))
    with open(sql_file, "r") as f:
        cursor.execute(f.read())
    

    # debug to check whole database is there
    cursor.execute("Select * from adm")
    results = cursor.fetchall()
    for result in results:
        print(result)
