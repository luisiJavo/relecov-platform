import dash_html_components as html
import pandas as pd

# plotly dash
import dash_core_components as dcc
# import dash_html_components as html
from django_plotly_dash import DjangoDash

# import plotly.graph_objects as go
import plotly.express as px

# import pandas as pd

# from dash import Input, Output#Dash, dcc, html,
# from dash.dependencies import Input, Output
# import dash

# import dash_bootstrap_components as dbc
import os
from django.conf import settings

# IMPORT FROM UTILS
from relecov_core.utils.random_data import generate_random_sequences
# from relecov_core.utils.parse_files import *
# from relecov_core.utils.dashboard import *

# replaces dash.Dash
app = DjangoDash("SimpleExampleRangeSlider")


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


def get_variant_graph(variant_data):
    max_weeks = 0
    selected_range = [1, 19]
    df_table = pd.read_csv(
        os.path.join(
            settings.BASE_DIR, "relecov_core", "docs", "cogUK", "table_3_2022-04-12.csv"
        )
    )

    df = set_dataframe_range_slider(variant_data, selected_range)

    for week in df["Week"].unique():
        max_weeks += 1
    # replaces dash.Dash
    # app = DjangoDash("SimpleExampleRangeSlider")

    fig = px.bar(df, x="Week", y="Sequences", color="Variant", barmode="stack")

    return html.Div(
        className="card",
        children=[
            html.Div(
                className="card-body bg-light",
                children=[
                    html.H1(
                        className="card-title",
                        children="VOCs/VUIs in Spain",
                    ),
                    html.Div(
                        className="card-text",
                        children="Variant data.",
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
                                children="Variants of concern (VOC) and under investigation (VUI) detected in the Spain data.",
                                className="card-title",
                            ),
                            html.H5(
                                children="DISCLAIMER: relecov-platform uses curated sequences for determining the counts of a given lineage. Other sources of information may be reporting cases with partial sequence information or other forms of PCR testing.",
                                className="card-text",
                            ),
                        ],
                    )
                ],
            ),
            html.Div(
                children=generate_table(df_table),
            ),
        ],
    )
