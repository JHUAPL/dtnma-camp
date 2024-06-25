import psycopg2
import unittest

# from .util import TmpDir
from camp.tools.camp import run

class TestSQL(unittest.TestCase):
   
    @classmethod
    def setUpClass(self):
        # connect to ANMS library
        # params: https://gitlab.jhuapl.edu/anms/anms#amp-database-querying
        self._conn = psycopg2.connect(
                host="localhost",
                port=5432,
                # database="amp_core",
                user="postgres",
                password="root"
        )
        self.cursor = self._conn.cursor()

    @classmethod
    def tearDownClass(self):
        self.cursor.close()
        self._conn.close()

    # TODO which files to use? how many files? 1 file = 1 test case?
    #      using existing file for now...
    def test_ADM_AMP_AGENT(self):
        with open("amp-sql/Agent_Scripts/adm_amp_agent.sql", "r") as f:
            self.cursor.execute(f.read())

        # TODO assert something?
