# test cases for initws assignment
# Author: Nishanth Koganti
# Date: 2020/3/15

# import modules
import pytest

# relative imports
from aml.utils import set_env_vars, get_svc_pr, get_ws


@pytest.mark.local
@pytest.mark.parametrize('config_path', ['aml_scripts/.aml_config/config.json'])
def test_env_vars(config_path):
    # set env variables
    status = set_env_vars(config_path)

    # check the status
    assert status


@pytest.mark.cicd
@pytest.mark.local
def test_authentication():
    # perform service principal authentication
    svc_pr = get_svc_pr()

    # check the authentication
    assert svc_pr


@pytest.mark.cicd
@pytest.mark.local
def test_ws_init():
    # perform service principal authentication
    svc_pr = get_svc_pr()

    # connect to workspace
    ws = get_ws(svc_pr)

    # check the authentication
    assert ws
