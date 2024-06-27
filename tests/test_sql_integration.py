import psycopg2
import unittest
import argparse
import os

from .util import TmpDir
from camp.tools.camp import run

SELFDIR = os.path.dirname(__file__)

class TestSQL(unittest.TestCase):
   
    @classmethod
    def setUpClass(self):
        # connect to ANMS library
        # params: https://gitlab.jhuapl.edu/anms/anms#amp-database-querying
        self._conn = psycopg2.connect(
                host="127.0.0.1",
                port=5432,
                user="postgres",
                password="root"
        )
        self.cursor = self._conn.cursor()

    @classmethod
    def tearDownClass(self):
        self.cursor.close()
        self._conn.close()

    def setUp(self):
        self.maxDiff = None
        self._dir = TmpDir()
        # self._admset = AdmSet()

    def tearDown(self):
        del self._dir

    def _runCamp(self, filepath, outpath):
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
    def test_adms(self):
        adms_dir = os.path.join(SELFDIR, "data", "adms")
        adms = [f for f in os.listdir(adms_dir) if os.path.isfile(os.path.join(adms_dir, f))]

        for f in adms:
            filepath = os.path.join(adms_dir, f)

            # exitcode = self._runCamp(filepath, outpath)
            # self.assertEqual(0, exitcode)

            # with open("./amp-sql/Agent_Scripts/adm_amp_agent.sql", "r") as f:
            #     self.cursor.execute(f.read())
            
            # self.cursor.execute("Select * from adm")
            # results = self.cursor.fetchall()

        # for result in results:
        #     print(result)

        # # TODO assert something?

