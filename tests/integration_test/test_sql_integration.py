import psycopg2
import os
import ace
import pytest

from .util import _run_camp, ADMS_DIR


@pytest.fixture(scope="session", autouse=True)
def setup():
    """
    Connects to the ADMS library session. Cleans up connections once done.
    @pre: IP Address of the library session should be stored in env var $PGHOST,
          username and password should be stored in env vars $PGSQL_USERNAME and
          $PGSQL_PASSWORD, respectively
    @yields tuple of (connection object, AdmSet())
    """

    # setup: connect to ANMS library
    conn = psycopg2.connect(
            host=os.environ["PGHOST"],
            port=5432,
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"]
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
    exitcode = _run_camp(filepath, ADMS_DIR, only_sql=True, only_ch=False)
    assert 0 == exitcode

    # execute sql
    norm_name = admset.load_from_file(filepath).norm_name
    sql_file = os.path.join(ADMS_DIR, "amp-sql", "Agent_Scripts", 'adm_{name}.sql'.format(name=norm_name))
    with open(sql_file, "r") as f:
        cursor.execute(f.read())
