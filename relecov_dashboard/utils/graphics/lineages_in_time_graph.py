import os

from django.conf import settings
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# from relecov_core.utils.parse_files import parse_csv_into_list_of_dicts


def testing_fisabio_data():
    input_file = os.path.join(
        settings.BASE_DIR, "relecov_core", "docs", "fisabio_data.csv"
    )
    df = read_mutation_data(input_file, file_extension="csv")
    df = df.sort_values(by=["sample_collection_date"])
    # print(df)
    # create_test_variant_graph(df)
    create_lineage_in_time_graph(input_file, df)


def read_mutation_data(input_file: str, file_extension: str = "csv") -> pd.DataFrame:
    """
    Read fisabio.csv data, either in CSV format.
    Returns a pandas dataframe object
    """
    df = None
    if file_extension == "csv":
        df = pd.read_csv(input_file, sep=",")
    else:
        raise Exception("Unrecognized file format!")

    return df


def create_lineage_in_time_graph(input_file, df):
    app = DjangoDash(name="TestVariantGraph")
    app.layout = create_test_variant_graph(df)

    @app.callback(Output("graph-with-slider", "figure"), Input("date_slider", "value"))
    def update_figure(selected_range):
        df = read_mutation_data(input_file, file_extension="csv")

        # Create figure
        # fig = go.Figure()

        fig = make_subplots(1, 2)

        # add first bar trace at row = 1, col = 1

        fig.add_trace(
            go.Bar(
                x=df["sample_collection_date"],
                y=df["lineage_name"],
                name="A",
                marker_color="green",
                opacity=0.4,
                marker_line_color="rgb(8,48,107)",
                marker_line_width=2,
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=df["sample_collection_date"],
                y=df["lineage_name"],
                line=dict(color="red"),
                name="B",
            ),
            row=1,
            col=1,
        )

        """
        # add first bar trace at row = 1, col = 2
        fig.add_trace(go.Bar(x=df['sample_collection_date'], y=df['lineage_name'],
            name='C',
            marker_color = 'green',
            opacity=0.4,
            marker_line_color='rgb(8,48,107)',
            marker_line_width=1),
            row = 1, col = 2)
        """
        """
        fig = px.bar(
            df,
            x="sample_collection_date",
            y="lineage_name",
            color="who_name",
            barmode="stack",
            # hover_name="Variant",
        )
        """

        # fig.add_trace(
        # go.Scatter(x=list(df.sample_collection_date), y=list(df.lineage_name)))
        # Set title
        # fig.update_layout(title_text="Time series with range slider and selectors")

        # Add range slider
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
        # fig.update_layout(transition_duration=500)

        return fig


def create_test_variant_graph(df):
    date = 0
    # lineage=""
    # df = set_dataframe_range_slider(get_variant_data(), selected_range)
    list_of_dates = []
    list_of_lineages = []
    for date in df["sample_collection_date"].unique():
        list_of_dates.append(date.strip())
    for lineage in df["lineage_name"].unique():
        list_of_lineages.append(lineage)
    print(list_of_lineages)
    fig = px.bar(
        df,
        x="sample_collection_date",
        y="lineage_name",
        color="who_name",
        barmode="stack",
    )
    # pdb.set_trace()
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
                    min="2020-03-15",
                    max="2022-03-13",
                    step=None,
                    # type="date",
                    value=df["sample_collection_date"],
                    # value=[int(df["Week"].min()), max_weeks],
                    marks={
                        str(list_of_dates[idx]): {
                            "label": "{}".format(list_of_dates[idx]),
                            "style": {"transform": "rotate(45deg)", "margin": "5px"},
                        }
                        for idx in range(len(list_of_dates))
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
