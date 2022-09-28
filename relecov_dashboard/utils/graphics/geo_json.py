import os
import pandas as pd
import json
import plotly.express as px

import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
from relecov_platform import settings


def parse_json_file():
    """
    This function loads a json file and returns a python dictionary.
    """
    list_of_ccaa = []
    list_of_number_of_samples = []
    list_of_lists = []
    input_file = os.path.join(
        settings.BASE_DIR,
        "relecov_core",
        "docs",
        "data_for_geomap_from_ISkyLims_only_region.json",
    )
    with open(input_file) as f:
        data = json.load(f)
    
    region_data = data["region"]
    list_of_ccaa = region_data.keys()
    list_of_number_of_samples = region_data.values()

    list_of_lists.append(list_of_ccaa)
    list_of_lists.append(list_of_number_of_samples)

    df = pd.DataFrame(list_of_lists).transpose()
    df.columns = ["CCAA", "NUMBER_OF_SAMPLES"]
    df = df.sort_values(by=["NUMBER_OF_SAMPLES"])

    return df


def create_json(lineage):
    ldata = parse_json_file()

    geojson_file = os.path.join(
        settings.BASE_DIR, "relecov_core", "docs", "spain-communities.geojson"
    )

    with open(geojson_file) as geo_json:
        counties = json.load(geo_json)
    # print(counties)
    """
    csv_file = os.path.join(
        settings.BASE_DIR, "relecov_core", "docs", "variants_long_table_last.csv"
    )
    with open(csv_file) as f:
        csv_data = parse_csv(f)

    json_file = os.path.join(
        settings.BASE_DIR,
        "relecov_core",
        "docs",
        "processed_metadata_lab_20220208_20220613.json",
    )
    json_data = parse_json_file(json_file)

    dict_of_samples = get_list_of_dict_of_lineages_from_long_table(csv_data)
    ldata = set_dataframe_geo_plot(
        preprocess_json_data_with_csv(json_data, csv_data), lineage
    )
    """
    fig = px.choropleth_mapbox(
        ldata,
        geojson=counties,
        locations=ldata.CCAA,
        color=ldata.NUMBER_OF_SAMPLES,
        color_continuous_scale="Viridis",
        range_color=(0, ldata.NUMBER_OF_SAMPLES.max()),
        mapbox_style="carto-positron",
        zoom=3,
        center={"lat": 35.9, "lon": -5.3},
        opacity=0.5,
        labels={"Count": "count rate"},
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    app = DjangoDash("geo_json")
    app.layout = html.Div(
        children=[
            html.Div(
                children=dcc.Graph(figure=fig, id="geomap-per-lineage"),
            ),
        ],
    )
    # ])

    @app.callback(
        Output("geomap-per-lineage", "figure"),
        Input("geomap-select-lineage", "value"),
    )
    def update_sample(selected_lineage):
        # lineage_by_ccaa = preprocess_json_data_with_csv(json_data, csv_data)
        # ldata = set_dataframe_geo_plot(lineage_by_ccaa, selected_lineage)
        ldata = parse_json_file()
        fig = px.choropleth_mapbox(
            data_frame=ldata,
            geojson=counties,
            locations=ldata.CCAA,
            color=ldata.NUMBER_OF_SAMPLES,
            color_continuous_scale="Viridis",
            range_color=(0, ldata.NUMBER_OF_SAMPLES.max()),
            mapbox_style="carto-positron",
            zoom=5,
            center={"lat": 35.9, "lon": -5.3},
            opacity=0.5,
            labels={"Count": "Number of samples"},
        )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
