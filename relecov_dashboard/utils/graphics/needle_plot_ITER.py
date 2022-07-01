import json
import os
from django.conf import settings
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output
import dash_bio as dashbio
import pandas as pd


def parse_csv(file_path):
    """
    fields => SAMPLE(0), CHROM(1), POS(2), REF(3), ALT(4),
    FILTER(5), DP(6),  REF_DP(7), ALT_DP(8), AF(9), GENE(10),
    EFFECT(11), HGVS_C(12), HGVS_P(13), HGVS_P1LETTER(14),
    CALLER(15), LINEAGE(16)
    """
    df = pd.read_csv(file_path, sep=",")

    return df


def set_dataframe_needle_plot(df, lineage):
    """
    This function receives a python dictionary, a list of selected fields and sets a dataframe from fields_selected_list
    to represent the graph dataframe structure(dict) { x: [], y: [], domains: [], mutationGroups: [],}
    """
    if lineage is None:
        first_line = df.iloc[0]
        lineage = first_line.at[0, "LINEAGE"]

    filter_df = df[df.LINEAGE == lineage]

    DOMAINS = [
        {"name": "orf1a", "coord": "265-13468"},
        {"name": "orf1b", "coord": "13468-21555"},
        {"name": "Spike", "coord": "21563-25384"},
        {"name": "orf3a", "coord": "25393-26220"},
        {"name": "E", "coord": "26245-26472"},
        {"name": "M", "coord": "26523-27191"},
        {"name": "orf6", "coord": "27202-27387"},
        {"name": "orf7a", "coord": "27394-27759"},
        {"name": "orf8", "coord": "27894-28259"},
        {"name": "N", "coord": "28274-29533"},
        {"name": "orf10", "coord": "29558-29674"},
    ]
    plot_df = {
        "x": filter_df.POS.to_list(),
        "y": filter_df.AF.to_list(),
        "domains": DOMAINS,
        "mutationGroups": filter_df.EFFECT.to_list(),
    }

    return plot_df


def parse_json_file(json_file):
    """
    This function loads a json file and returns a python dictionary.
    """
    json_parsed = {}
    # f = open(json_file)
    with open(json_file) as f:
        json_parsed["data"] = json.load(f)

    return json_parsed


def get_list_of_keys(json_parsed):
    list_of_keys = list(json_parsed["data"].keys())
    return list_of_keys


def create_graphic(data_frame):
    """
    This function represents a graph from a dataframe
    """
    # data = parse_json_file()
    # dataframe = set_dataframe()
    pass


def get_list_of_dict_of_lineages_from_long_table(df):
    """
    This function receives parsed file from parse_csv().
    Returns a list of dictionaries of lineages [{"label": "B.1.177.57", "value": "B.1.177.57"}]
    """
    unique_lineages = df.LINEAGE.unique()
    list_of_lineages = []
    for lin in unique_lineages:
        list_of_lineages.append({"label": lin, "value": lin})

    return list_of_lineages


def create_needle_plot_graph_ITER(lineage):
    needle_data = os.path.join(
        settings.BASE_DIR, "relecov_core", "docs", "variants_long_table_last.csv"
    )
    dict_of_samples = get_list_of_dict_of_lineages_from_long_table(
        parse_csv(needle_data)
    )
    mdata = set_dataframe_needle_plot(parse_csv(needle_data), lineage)
    # app = DjangoDash("needle_plot")
    app = DjangoDash("needle_plot_ITER")
    app.layout = html.Div(
        children=[
            "Show or hide range slider",
            dcc.Dropdown(
                id="needleplot-rangeslider",
                options=[{"label": "Show", "value": 1}, {"label": "Hide", "value": 0}],
                clearable=False,
                multi=False,
                value=1,
                # style={"width": "400px"},
            ),
            "Select a Lineage",
            dcc.Dropdown(
                id="needleplot-select-lineage",
                options=dict_of_samples,
                clearable=False,
                multi=False,
                value=lineage,
                # style={"width": "400px"},
            ),
            html.Div(
                children=dashbio.NeedlePlot(
                    width="auto",
                    id="dashbio-needleplot",
                    xlabel="Genome Position",
                    ylabel="Allele Frequency ",
                    mutationData=mdata,
                    domainStyle={
                        # "textangle": "45",
                        "displayMinorDomains": True,
                        "domainColor": [
                            "#FFDD00",
                            "#00FFDD",
                            "#0F0F0F",
                            "#D3D3D3",
                            "#FFDD00",
                            "#00FFDD",
                            "#0F0F0F",
                            "#D3D3D3",
                            "#FFDD00",
                            "#00FFDD",
                            "#0F0F0F",
                        ],
                    },
                    needleStyle={
                        "stemColor": "#444",
                        "stemThickness": 0.5,
                        "stemConstHeight": False,
                        "headSize": 5,
                        "headColor": [
                            "#e41a1c",
                            "#377eb8",
                            "#4daf4a",
                            "#984ea3",
                            "#ff7f00",
                            "#ffff33",
                            "#a65628",
                            "#f781bf",
                            "#999999",
                            "#e41a1c",
                            "#377eb8",
                            "#4daf4a",
                            "#984ea3",
                            "#ff7f00",
                            "#ffff33",
                            "#a65628",
                            "#f781bf",
                            "#999999",
                            "#e41a1c",
                        ],
                        "headSymbol": "circle",
                    },
                ),
            ),
        ],
    )

    @app.callback(
        Output("dashbio-needleplot", "mutationData"),
        Input("needleplot-select-lineage", "value"),
    )
    def update_sample(selected_lineage):
        print(selected_lineage)
        create_needle_plot_graph_ITER(selected_lineage)
        mdata = set_dataframe_needle_plot(parse_csv(needle_data), selected_lineage)
        mutation_data = mdata
        return mutation_data

    @app.callback(
        Output("dashbio-needleplot", "rangeSlider"),
        Input("needleplot-rangeslider", "value"),
    )
    def update_range_slider(range_slider_value):
        print(range_slider_value)
        return True if range_slider_value else False
