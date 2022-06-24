import os
import random
import json
from django.conf import settings
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from relecov_core.utils.parse_files import parse_csv_into_list_of_dicts

"""
from relecov_core.core_config import (
    BIOINFO_UPLOAD_FOLDER,
    ERROR_INVALID_JSON,
)
"""


def generate_random_sequences():
    sequence_list = []
    for i in range(103):
        sequence = random.randint(100, 1000)
        sequence_list.append(sequence)
    return sequence_list


def generate_weeks():
    weeks_list = []

    for j in range(10):
        weeks_list.append(1)
    for k in range(10):
        weeks_list.append(2)
    for la in range(10):
        weeks_list.append(3)
    for m in range(10):
        weeks_list.append(4)
    for n in range(10):
        weeks_list.append(5)
    for o in range(10):
        weeks_list.append(6)
    for p in range(10):
        weeks_list.append(7)
    for q in range(10):
        weeks_list.append(8)
    for r in range(10):
        weeks_list.append(9)
    for s in range(10):
        weeks_list.append(10)
    for t in range(3):
        weeks_list.append(11)

    return weeks_list


def parse_json_file(json_file):
    data = {}
    # try:
    data = json.loads(json_file)
    # except json.decoder.JSONDecodeError:
    #    return {"ERROR": ERROR_INVALID_JSON}
    # data["file_name"] = store_file(json_file, BIOINFO_UPLOAD_FOLDER)
    return data


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


def get_variant_data():
    variant_data = parse_csv_into_list_of_dicts(
        os.path.join(
            settings.BASE_DIR, "relecov_core", "docs", "variantLuisTableCSV.csv"
        )
    )
    return variant_data


def create_lineage_in_time_graph():
    app = DjangoDash(name="TestVariantGraph")
    app.layout = create_test_variant_graph([1, 19])

    @app.callback(Output("graph-with-slider", "figure"), Input("week-slider", "value"))
    def update_figure(selected_range):
        df = set_dataframe_range_slider(get_variant_data(), selected_range)

        fig = px.bar(
            df,
            x="Week",
            y="Sequences",
            color="Variant",
            barmode="stack",
            hover_name="Variant",
        )

        fig.update_layout(transition_duration=500)

        return fig


def create_test_variant_graph(selected_range):
    max_weeks = 0
    df = set_dataframe_range_slider(get_variant_data(), selected_range)

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
