import psycopg2
import argparse
import os
import ace
import pytest

from camp.tools.camp import run

ADMS_DIR = os.path.join("tests", "adms")

@pytest.fixture(scope="session", autouse=True)
def setup(ip):
    """
    Connects to the ADMS library session. Cleans up connections once done.
    @param ip: IP address of the library connection. Can be determined through
      port-mapping when creating the library, or checking the docker container
      (docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container_name>)
    @yields tuple of (connection object, AdmSet())
    """

    # setup: connect to ANMS library
    conn = psycopg2.connect(
            host=ip, # TODO might need to change? or pass through somehow?
            port=5432,
            user="postgres",
            password="root"
    )
    cursor = conn.cursor()
    
    # reusable objects that the tests will need
    admset = ace.AdmSet()
    yield cursor, admset

    # teardown: close connections
    cursor.close()
    conn.close()


@pytest.mark.parametrize("adm", [f for f in os.listdir(ADMS_DIR) if os.path.isfile(os.path.join(ADMS_DIR, f))])
def test_adms(setup, adm):
    """
    Integration test for an ADM found in the ADMS_DIR folder
    Resulting sql files will be placed in ADMS_DIR/amp-sql/Agent_Scripts and executed in the anms library.
    """
    cursor = setup[0]
    admset = setup[1]

    # ensure file is .json or .yang (and not the index.json file)
    ext = os.path.splitext(adm)[1]
    if (ext != ".json" and ext != ".yang") or adm == "index.json":
        pytest.skip("file skipped: {f} is not an adm file".format(f=adm))

    # run camp
    filepath = os.path.join(ADMS_DIR, adm)
    exitcode = runCamp(filepath, ADMS_DIR)
    assert 0 == exitcode

    # execute sql
    norm_name = admset.load_from_file(filepath).norm_name
    sql_file = os.path.join(ADMS_DIR, "amp-sql", "Agent_Scripts", 'adm_{name}.sql'.format(name=norm_name))
    with open(sql_file, "r") as f:
        cursor.execute(f.read())


def runCamp(filepath, outpath):
    """
    Generates sql files by running CAmp on filepath. Resulting sql files are stored
    in outpath
    """
    args = argparse.Namespace()
    args.admfile = filepath
    args.out = outpath
    args.only_sql = True
    args.only_ch = False
    return run(args)
