import json

# import pandas as pd
# import dash_core_components as dcc
import dash_html_components as html

# import plotly.express as px
"""
from relecov_core.core_config import (
    BIOINFO_UPLOAD_FOLDER,
    ERROR_INVALID_JSON,
)
"""


def parse_json_file(json_file):
    """
    This function loads a json file and returns a python dictionary.
    """
    data = {}
    f = open(json_file)
    data["data"] = json.load(f)

    return data


def set_dataframe(data_dictionary, fields_selected_list):
    """
    This function receives a python dictionary, a list of selected fields and sets a dataframe from fields_selected_list to represent the graph
    """
    pass


def create_graphic(data_frame):
    """
    This function represents a graph from a dataframe
    """
    # data = parse_json_file()
    # dataframe = set_dataframe()
    pass


def generate_table(dataframe, max_rows=14):
    return html.Table(
        className="table table-striped",
        children=[
            html.Thead(
                className="table-info",
                children=html.Tr([html.Th(col) for col in dataframe.columns]),
            ),
            html.Tbody(
                [
                    html.Tr(
                        [html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]
                    )
                    for i in range(min(len(dataframe), max_rows))
                ],
            ),
        ],
    )
