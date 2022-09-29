from datetime import datetime
import os
from time import strptime

# import random
import json
from django.conf import settings
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from relecov_core.models import DateUpdateState

# from relecov_core.utils.parse_files import parse_csv_into_list_of_dicts


def create_dataframe_from_database():
    """
    This function reads data from database, "DateUpdateState" model,
    and creates a pandas dataframe object with this fields:
        -"SAMPLE" -> from "sampleID" field
        -"DATE"   -> from "date" field
    """
    sample_objs = DateUpdateState.objects.all()
    date_list = []
    list_of_dates = []
    list_of_samples = []
    list_of_lists = []
    for sample_obj in sample_objs:
        list_of_samples.append(sample_obj.get_sample_id())
        date = sample_obj.get_date()
        date_list = date.split(",")
        year = date_list[1]
        date_list = date_list[0].split(" ")
        month = strptime(date_list[0], "%B").tm_mon
        date_converted = datetime(int(year), month, int(date_list[1]))
        list_of_dates.append(date_converted.strftime("%Y-%m-%d"))

    list_of_lists.append(list_of_samples)
    list_of_lists.append(list_of_dates)

    df = pd.DataFrame(list_of_lists).transpose()
    df.columns = ["SAMPLE", "DATE"]
    df = df.sort_values(by=["DATE"])

    return df


def create_dataframe_from_json():
    """
    This function reads data from file "processed_converted_metadata_lab.json",
    and creates a pandas dataframe object with this fields:
        -"SAMPLE" -> from "isolate_sample_id" field
        -"DATE"   -> from "sample_received_date"
    """

    list_of_samples = []
    list_of_dates = []
    list_of_lists = []
    input_file = os.path.join(
        settings.BASE_DIR,
        "relecov_core",
        "docs",
        "processed_converted_metadata_lab.json",
    )
    with open(input_file) as f:
        data = json.load(f)

    for line in data:
        list_of_samples.append(line["isolate_sample_id"])
        list_of_dates.append(line["sample_received_date"])

    list_of_lists.append(list_of_samples)
    list_of_lists.append(list_of_dates)

    df = pd.DataFrame(list_of_lists).transpose()
    df.columns = ["SAMPLE", "DATE"]
    df = df.sort_values(by=["DATE"])

    return df


def create_lineage_in_time_graph(df):
    app = DjangoDash(name="TestVariantGraph")
    app.layout = create_test_variant_graph(df)

    @app.callback(Output("graph-with-slider", "figure"), Input("date_slider", "value"))
    def update_figure(selected_range):
        # df = create_dataframe_variants_in_time
        df = create_dataframe_from_json()
        print(df)

        fig = px.bar(
            df,
            x="DATE",
            y="SAMPLE",
            color="DATE",
            barmode="stack",
            # hover_name="Variant",
        )

        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1, label="1m", step="month", stepmode="backward"
                            ),
                            dict(
                                count=6, label="6m", step="month", stepmode="backward"
                            ),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=True),
                type="date",
            )
        )

        fig.update_layout(transition_duration=500)

        return fig


def create_test_variant_graph(df):
    fig = px.bar(
        df,
        x="DATE",
        y="SAMPLE",
        color="DATE",
        barmode="stack",
    )

    return html.Div(
        className="card",
        children=[
            html.Div(
                className="card-body bg-dark",
                children=[
                    html.H1(
                        className="card-title",
                        children="Linages in Spain",
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
                    id="date_slider",
                    min=1,
                    max=3,
                    step=None,
                    # type="date",
                    value=df["DATE"],
                    # value=[int(df["Week"].min()), max_weeks],
                    marks=None,
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
            # html.Div(children=generate_table(df_table)),
        ],
    )
