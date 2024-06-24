import camp
import psycopg2
import unittest


class TestSQL(unittest.TestCase):
   
    @classmethod
    def setUpClass(self):
        # connect to ANMS library
        # params: https://gitlab.jhuapl.edu/anms/anms#amp-database-querying
        self._conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="amp_core",
                user="root",
                password="root"
            )
        self.cursor = self._conn.cursor()

    @classmethod
    def tearDownClass(self):
        self.cursor.close()
        self._conn.close()

    # TODO which files to use? how many files? 1 file = 1 test case?
    #      using existing file for now...
    def test_ADM_IETF_DTNMA_AGENT(self):
        with open("amp-sql/Agent_Scripts/adm_ietf-dtnma-agent.sql", "r") as f:
            self.cursor.execute(f.read())

        # TODO assert something?

    # def test_ADM_AMP_AGENT(self):
    #     with open("amp-sql/Agent_Scripts/adm_amp_agent.sql", "r") as f:
    #         self.cursor.execute(f.read())

    #     # TODO assert something?
