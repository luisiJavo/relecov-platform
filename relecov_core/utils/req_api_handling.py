from relecov_tools.rest_api import RestApi
from relecov_core.utils.generic_functions import get_configuration_value
from relecov_core.core_config import (
    ISKLIMS_GET_LABORATORY_PARAMETERS,
    ISKLIMS_PUT_LABORATORY_PARAMETER,
    ISKLIMS_REST_API,
)


def get_laboratory_data(lab_name):
    """Send api request to iSkyLIMS to fetch laboratory data"""

    iskylims_server = get_configuration_value("ISKYLIMS_SERVER")
    iskylims_url = ISKLIMS_REST_API
    request, param = ISKLIMS_GET_LABORATORY_PARAMETERS
    r_api = RestApi(iskylims_server, iskylims_url)
    data = r_api.get_request(request, param, lab_name)
    if "ERROR" in data:
        return {"ERROR": data}
    return data


def set_laboratory_data(lab_data):
    """Send api request to iSkyLIMS to update laboratory data"""

    iskylims_server = get_configuration_value("ISKYLIMS_SERVER")
    iskylims_url = ISKLIMS_REST_API

    request, param = ISKLIMS_PUT_LABORATORY_PARAMETER
    r_api = RestApi(iskylims_server, iskylims_url)
    data = r_api.put_request(request, param, lab_data)
    if "ERROR" in data:
        return {"ERROR": data}
    return data
