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

@pytest.fixture()
def setup():
    # setup
    # connect to ANMS library
    conn = psycopg2.connect(
            host="172.17.0.3", # might need to change? or pass through somehow?
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


# class TestSQL():
   
    # def setUp(self):
    #     self.maxDiff = None
    #     self._dir = TmpDir()
    #     # self._admset = AdmSet()

    # def tearDown(self):
    #     del self._dir

def _runCamp(filepath, outpath):
    """
    Obtains sql files generated from running CAmp on filepath. Moves to temp directory
    """
    args = argparse.Namespace()
    args.admfile = filepath
    args.out = outpath
    args.only_sql = True
    args.only_ch = False
    return run(args)


# TODO which files to use? how many files? 1 file = 1 test case?
#      using existing file for now...
@pytest.mark.parametrize("f", [f for f in os.listdir(ADMS_DIR) if os.path.isfile(os.path.join(ADMS_DIR, f))])
def test_adms(setup, f):
    """
    Integration test for all the ADMs found in the ADMS_DIR folder
    Resulting sql files will be placed in ADMS_DIR/amp-sql/Agent_Scripts
    """
    print(setup)
    cursor = setup[0]
    admset = setup[1]

    # for f in adms:
    filepath = os.path.join(ADMS_DIR, f)
    print(filepath)

    exitcode = _runCamp(filepath, ADMS_DIR)
    assert 0 == exitcode

    norm_name = admset.load_from_file(filepath).norm_name
    sql_file = os.path.join(ADMS_DIR, "amp-sql", "Agent_Scripts", f'adm_{norm_name}.sql')
    print(sql_file)
    with open(sql_file, "r") as f:
        cursor.execute(f.read())
    
    cursor.execute("Select * from adm")
    results = cursor.fetchall()

    for result in results:
        print(result)
