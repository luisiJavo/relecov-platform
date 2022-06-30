"""
Mutation table under needle plot
- Read JSON/CSV
- Generate dataframe
- Clean or filter dataframe
- Generate auxiliar table to needle plot
"""


# Dash libs
import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# Other libs
import pandas as pd
import json


def read_data(input_file: str, file_extension: str = "csv") -> pd.DataFrame:
    """
    Read data, either in CSV or JSON format.
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


def process_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process pd.DataFrame object, selecting specific columns and renaming then as required
    (maybe usefull for translations)
    """
    translate_dicc = {
        "SAMPLE": "SAMPLE",
        "POS": "POS",
        "AF": "AF",
        "EFFECT": "EFFECT",
        "GENE": "GENE",
        "LINEAGE": "LINEAGE",
    }
    # Rename and select columns
    df = df[translate_dicc.keys()]  # select specific keys
    df = df.rename(columns=translate_dicc)  # rename to the required output names

    return df


def create_mutation_table(sample):
    pass


# ---- Set up ----
# Input
input_file = (
    "/home/usuario/Proyectos/relecov/relecov-platform/data/variants_long_table.csv"
)
sample_id = 214821

# Read data
df = read_data(input_file, file_extension="csv")
df = process_df(df)

# Read some extra values
all_effects = list(df["EFFECT"].unique())
all_genes = list(df["GENE"].unique())
sample_ids = list(df["SAMPLE"].unique())


# ---- Dash app ----
app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.P(id="mutation_table-message"),
        html.Div(
            style={
                "display": "flex",
                "justify-content": "start",
                "align-items": "flex-start",
            },
            children=[
                dcc.Dropdown(
                    id="mutation_table-effect_dropdown",
                    options=[{"label": i, "value": i} for i in all_effects],
                    clearable=False,
                    multi=True,
                    value=None,
                    style={"width": "200px", "margin-right": "30px"},
                    placeholder="Filter effect",
                ),
                dcc.Dropdown(
                    id="mutation_table-gene_dropdown",
                    options=[{"label": i, "value": i} for i in all_genes],
                    clearable=False,
                    multi=True,
                    value=None,
                    style={"width": "200px", "margin-right": "30px"},
                    placeholder="Filter genes",
                ),
                dcc.Dropdown(
                    id="needleplot-select-sample",
                    options=[{"label": i, "value": i} for i in sample_ids],
                    clearable=False,
                    multi=False,
                    value=sample_id,
                    style={"width": "200px", "margin-right": "30px"},
                ),
            ],
        ),
        html.Br(),
        dash_table.DataTable(
            id="mutation_table",
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
        ),
    ]
)


def update_selected_effects(data: pd.DataFrame, selected_effects: list):
    if (
        selected_effects
        and type(selected_effects) == list
        and len(selected_effects) >= 1
    ):
        data = data[data["EFFECT"].isin(selected_effects)]
    return data


def update_selected_sample(data: pd.DataFrame, selected_sample: int):
    if selected_sample and type(selected_sample) == int:
        data = data[data["SAMPLE"].isin([selected_sample])]
    return data


def update_selected_genes(data: pd.DataFrame, selected_genes: int):
    if selected_genes and type(selected_genes) == list and len(selected_genes) >= 1:
        data = data[data["GENE"].isin(selected_genes)]
    return data


@app.callback(
    Output("mutation_table", "data"),
    Input("needleplot-select-sample", "value"),
    Input("mutation_table-effect_dropdown", "value"),
    Input("mutation_table-gene_dropdown", "value"),
)
def update_graph(
    sample: str, effects: list, genes: list
):  # Order of arguments MUST be the same as in the callback function
    data = df
    data = update_selected_effects(data, effects)
    data = update_selected_sample(data, sample)
    data = update_selected_genes(data, genes)

    return data.to_dict("records")


@app.callback(
    Output("mutation_table-message", "children"), Input("mutation_table", "active_cell")
)
def show_clicks(active_cell):
    # TODO: Influence needle plot, maybe highlighting the mutation (?)
    if active_cell:
        return str(active_cell)
    else:
        return "Click the table"


if __name__ == "__main__":
    app.run_server(debug=True)
