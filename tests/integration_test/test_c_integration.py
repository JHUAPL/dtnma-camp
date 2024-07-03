import pytest
import os

from .util import _run_camp

ADMS_DIR = os.path.join("tests", "adms")  # TODO may move to util if same


@pytest.mark.parametrize("adm", ["amp_agent.json"])
def test_adms(adm):

    filepath = os.path.join(ADMS_DIR, adm)
    exitcode = _run_camp(filepath, ADMS_DIR, only_sql=False, only_ch=True, scrape=False)
    assert 0 == exitcode

    print(adm)