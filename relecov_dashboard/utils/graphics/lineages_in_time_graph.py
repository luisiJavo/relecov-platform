import os

# import random
import json
from django.conf import settings
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from relecov_core.utils.parse_files import parse_csv_into_list_of_dicts


def testing_fisabio_data():
    input_file = os.path.join(
        settings.BASE_DIR, "relecov_core", "docs", "fisabio_data.csv"
    )
    df = read_mutation_data(input_file, file_extension="csv")
    print(df)
    # create_test_variant_graph(df)
    create_lineage_in_time_graph(input_file, df)


def read_mutation_data(input_file: str, file_extension: str = "csv") -> pd.DataFrame:

    # Read mutation data, either in CSV or JSON format.
    # If in JSON format, the JSON must follow a structure of [{'pk': {'atr1':'z'} }]
    # Returns a pandas dataframe object

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


def create_lineage_in_time_graph(input_file, df):
    app = DjangoDash(name="TestVariantGraph")
    app.layout = create_test_variant_graph(df)

    @app.callback(Output("graph-with-slider", "figure"), Input("week-slider", "value"))
    def update_figure(selected_range):
        df = read_mutation_data(input_file, file_extension="csv")

        fig = px.bar(
            df,
            x="sample_collection_date",
            y="lineage_name",
            color="who_name",
            barmode="stack",
            # hover_name="Variant",
        )

        fig.update_layout(transition_duration=500)

        return fig


def create_test_variant_graph(df):
    max_weeks = 0
    # df = set_dataframe_range_slider(get_variant_data(), selected_range)
    list_of_weeks = []

    for week in df["sample_collection_date"].unique():
        # max_weeks += 1
        list_of_weeks.append(week.strip())

    fig = px.bar(
        df,
        x="sample_collection_date",
        y="lineage_name",
        color="who_name",
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
                    id="week-slider",
                    min=1,  # df["Week"].min(),
                    max=max_weeks,
                    step=None,
                    value=[1, 19],
                    # value=[int(df["Week"].min()), max_weeks],
                    marks={
                        str(list_of_weeks[idx]): {
                            "label": "{}º Week".format(list_of_weeks[idx]),
                            "style": {"transform": "rotate(45deg)", "margin": "5px"},
                        }
                        for idx in range(len(list_of_weeks))
                    },
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
