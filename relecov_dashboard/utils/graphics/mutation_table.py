"""
Mutation table under needle plot
- Read JSON/CSV
- Generate dataframe
- Clean or filter dataframe
- Generate auxiliar table to needle plot
"""


import os
import pandas as pd
import json

from django.conf import settings
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import dash_table


def read_mutation_data(input_file: str, file_extension: str = "csv") -> pd.DataFrame:
    """
    Read mutation data, either in CSV or JSON format.
    If in JSON format, the JSON must follow a structure of [{'pk': {'atr1':'z'} }]
    Returns a pandas dataframe object
    """
    df = None
    if file_extension == "json":
        with open(input_file) as f:
            # JSON must have a "primary key", which is the sample ID
            df = pd.DataFrame.from_dict(json.load(f), orient="index")
            df = df.reset_index().rename(columns={"index": "SAMPLE"})
    elif file_extension == "csv":
        df = pd.read_csv(input_file, sep=",")
    else:
        raise Exception("Unrecognized file format!")

    return df


def process_mutation_df(df: pd.DataFrame, renaming_dict: dict = None) -> pd.DataFrame:
    """
    Process pd.DataFrame object, selecting specific columns and renaming then as required
    (maybe usefull for translations)
    """
    if renaming_dict is None and type(renaming_dict) != dict:
        renaming_dict = {
            "SAMPLE": "SAMPLE",
            "POS": "POS",
            "HGVS_P": "MUTATION",
            "AF": "AF",
            "EFFECT": "EFFECT",
            "GENE": "GENE",
            "LINEAGE": "LINEAGE",
        }

    # Rename and select columns
    df = df[renaming_dict.keys()]  # select specific keys
    df = df.rename(columns=renaming_dict)  # rename to the required output names

    return df


def create_mutation_table(sample):
    PAGE_SIZE = 20

    input_file = os.path.join(
        settings.BASE_DIR, "relecov_core", "docs", "variants_long_table_last.csv"
    )

    # Read data
    df = read_mutation_data(input_file, file_extension="csv")
    df = process_mutation_df(df)

    # Read some extra values
    effects = list(df["EFFECT"].unique())

    app = DjangoDash("mutation_table")

    app.layout = html.Div(
        children=[
            html.P(id="mutation_table-message"),
            dcc.Dropdown(
                id="mutation_table-effect_dropdown",
                options=[{"label": i, "value": i} for i in effects],
                clearable=False,
                multi=True,
                value=1,
                style={"width": "400px"},
                placeholder="Mutation effect",
            ),
            html.Br(),
            dash_table.DataTable(
                id="mutation_table",
                data=df.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df.columns],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action="custom",
            ),
        ]
    )

    @app.callback(
        Output("mutation_table", "data"),
        Input("mutation_table-effect_dropdown", "value"),
    )
    def update_selected_effects(selected_effects):
        data = df
        if type(selected_effects) == list and len(selected_effects) >= 1:
            data = data[data["EFFECT"].isin(selected_effects)]
        return data.to_dict("records")

    @app.callback(
        Output("mutation_table-message", "children"),
        Input("mutation_table", "active_cell"),
    )
    def show_clicks(active_cell):
        if active_cell:
            return str(active_cell)
        else:
            return "Click the table"

    if __name__ == "__main__":
        app.run_server(debug=True)
