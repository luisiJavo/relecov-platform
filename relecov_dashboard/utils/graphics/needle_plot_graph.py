import json
import os
from django.conf import settings

import dash_core_components as dcc

# from dash import dcc

import dash_html_components as html

# from dash import ctx
from django_plotly_dash import DjangoDash

# from dash import ctx
from dash.dependencies import Input, Output
import dash_bio as dashbio


def parse_csv(file_path):
    """
    fields => SAMPLE(0), CHROM(1), POS(2), REF(3), ALT(4),
    FILTER(5), DP(6),  REF_DP(7), ALT_DP(8), AF(9), GENE(10),
    EFFECT(11), HGVS_C(12), HGVS_P(13), HGVS_P1LETTER(14),
    CALLER(15), LINEAGE(16)
    """
    # data_array = []  # one field per position
    # headers = []

    # variant_data = []
    # variant_fields = ["pos", "ref", "alt", "dp", "ref_dp", "alt_dp", "af"]
    # variant_pos = [2, 3, 4, 6, 7, 8, 9]

    # effect_fields = ["effect", "hgvs_c", "hgvs_p", "hgvs_p_1_letter"]
    # effect_pos = [11, 12, 13, 14]

    with open(file_path) as fh:
        lines = fh.readlines()

    # headers = lines[0].split(",")

    """
        data_dict = {"variant_dict": {}, "effect_dict": {}}
        for iv in range(len(variant_fields)):
            data_dict["variant_dict"][variant_fields[iv]] = data_array[variant_pos[iv]]
        # effect_dict = {}
        for ix in range(len(effect_fields)):
            data_dict["effect_dict"][effect_fields[ix]] = data_array[effect_pos[ix]]
        data_dict["filter"] = data_array[5]
        data_dict["chromosome"] = data_array[1]
        data_dict["sample"] = data_array[0]
        data_dict["caller"] = data_array[15]
        data_dict["lineage_dict"] = {"lineage": data_array[16], "week": data_array[17]}
        data_dict["gene"] = data_array[10]
        variant_data.append(data_dict)
    """
    return lines


def set_dataframe_needle_plot(lines_from_long_table, sample):  # , sample
    """
    This function receives a python dictionary, a list of selected fields and sets a dataframe from fields_selected_list to represent the graph
    dataframe structure(dict) { x: [], y: [], domains: [], mutationGroups: [],}
    """
    pos_list = []
    af_list = []
    effect_list = []
    gene_list = []
    if sample is None:
        first_line = lines_from_long_table[1].split(",")
        sample = first_line[0]
    df = {}

    for line in lines_from_long_table[1:]:
        data_array = line.split(",")
        if data_array[0] == sample:
            pos_list.append(data_array[2])
            af_list.append(data_array[9])
            effect_list.append(data_array[11])
            gene_list.append(data_array[10])

    df["x"] = pos_list
    df["y"] = af_list
    df["domains"] = [
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
    df["mutationGroups"] = effect_list

    return df


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


def get_list_of_dict_of_samples_from_long_table(lines):
    """
    This function receives parsed file from parse_csv().
    Returns a a list of dictionaries of samples [{"label": "220685", "value": "220685"}]
    """

    list_of_samples = []
    for line in lines[1:]:
        dict_of_samples = {}
        data_array = line.split(",")
        if (
            len(list_of_samples) == 0
            or {"label": data_array[0], "value": data_array[0]} not in list_of_samples
        ):
            dict_of_samples["label"] = data_array[0]
            dict_of_samples["value"] = data_array[0]
            list_of_samples.append(dict_of_samples)

    return list_of_samples


def create_needle_plot_graph(sample):
    needle_data = os.path.join(
        settings.BASE_DIR, "relecov_core", "docs", "variants_long_table_last.csv"
    )
    dict_of_samples = get_list_of_dict_of_samples_from_long_table(
        parse_csv(needle_data)
    )
    mdata = set_dataframe_needle_plot(parse_csv(needle_data), sample)
    app = DjangoDash("needle_plot")
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
            "Select a Sample",
            dcc.Dropdown(
                id="needleplot-select-sample",
                options=dict_of_samples,
                clearable=False,
                multi=False,
                value=sample,
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
        Input("needleplot-select-sample", "value"),
    )
    def update_sample(selected_sample):
        create_needle_plot_graph(selected_sample)
        mdata = set_dataframe_needle_plot(parse_csv(needle_data), selected_sample)
        mutationData = mdata
        return mutationData

    @app.callback(
        Output("dashbio-needleplot", "rangeSlider"),
        Input("needleplot-rangeslider", "value"),
    )
    def update_range_slider(range_slider_value):
        return True if range_slider_value else False
