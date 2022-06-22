import random
import json
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from relecov_core.core_config import (
    BIOINFO_UPLOAD_FOLDER,
    ERROR_INVALID_JSON,
)


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


def set_dataframe_range_slider(variant_data, selected_range):
    sequences_list = generate_random_sequences()
    lineage_list = []
    sequences_list2 = []
    lineage_week_list2 = []
    lineage_list2 = []

    for variant in variant_data:
        lineage_list.append(variant["lineage_dict"]["lineage"])
        if int(variant["lineage_dict"]["week"]) >= int(selected_range[0]) and int(
            variant["lineage_dict"]["week"]
        ) <= int(selected_range[1]):
            lineage_list2.append(variant["lineage_dict"]["lineage"])
            lineage_week_list2.append(variant["lineage_dict"]["week"])
    for i in range(len(lineage_list2)):
        sequences_list2.append(sequences_list[i])

    df = pd.DataFrame(
        {
            "Week": lineage_week_list2,
            "Sequences": sequences_list2,
            "Variant": lineage_list2,
        }
    )
    return df


def create_test_variant_graph(variant_data, selected_range):
    max_weeks = 0
    df = set_dataframe_range_slider(variant_data, selected_range)

    for week in df["Week"].unique():
        max_weeks += 1

    fig = px.bar(df, x="Week", y="Sequences", color="Variant", barmode="stack")

    return html.Div(
        className="card",
        children=[
            html.Div(
                className="card-body bg-light",
                children=[
                    html.H1(
                        className="card-title",
                        children="Dummy test values for Linages in Spain",
                    ),
                    html.Div(
                        className="card-text",
                        children="Linages evolution.",
                    ),
                ],
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            dcc.Graph(
                                className="card", id="graph-with-slider", figure=fig
                            )
                        ]
                    )
                ]
            ),
            html.Br(),
            html.Div(
                children=dcc.RangeSlider(
                    min=df["Week"].min(),
                    max=max_weeks,
                    step="1",
                    value=[int(df["Week"].min()), max_weeks],
                    marks={str(week): str(week) for week in df["Week"].unique()},
                    id="week-slider",
                ),
            ),
            html.Div(
                className="card bg-light",
                children=[
                    html.Div(
                        className="card-body",
                        children=[
                            html.H3(
                                children="Variants of concern"
                                + "(VOC) and under investigation"
                                + "(VUI) detected in the Spain data.",
                                className="card-title",
                            ),
                            html.H5(
                                children="DISCLAIMER: relecov-platform"
                                + "uses curated sequences"
                                + "for determining the counts"
                                + "of a given lineage. Other sources"
                                + "of information may be reporting"
                                + "cases with partial sequence"
                                + "information or other forms"
                                + "of PCR testing.",
                                className="card-text",
                            ),
                        ],
                    )
                ],
            ),
            # html.Div(children=generate_table(df_table),),
        ],
    )
