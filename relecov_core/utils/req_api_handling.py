from relecov_tools.rest_api import RestApi
from relecov_core.utils.generic_functions import get_configuration_value
from relecov_core.core_config import ISKLIMS_LABORATORY_PARAMETERS


def get_laboratory_data(lab_name):
    """Send api request to iSkyLIMS to fetch laboratory data"""

    iskylims_server = get_configuration_value("ISKYLIMS_SERVER")
    iskylims_url, req, param = ISKLIMS_LABORATORY_PARAMETERS
    r_api = RestApi(iskylims_server, iskylims_url)
    data = r_api.get_request(req, param, lab_name)
    if "ERROR" in data:
        return {"ERROR": data}
    return data
