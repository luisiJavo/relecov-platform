"""
Mutation table under needle plot
- Read JSON/CSV
- Generate dataframe
- Clean or filter dataframe
- Generate auxiliar table to needle plot
"""


import os
import pandas as pd
import json

from django.conf import settings
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash
import dash_table
from relecov_core.models import Effect, Gene, VariantAnnotation, VariantInSample

from relecov_core.utils.handling_variant import (
    # get_if_chromosomes_exists,
    # get_if_organism_exists,
    get_position_per_sample,
    get_alelle_frequency_per_sample,
    create_effect_list,
)
from relecov_core.utils.handling_samples import get_sample_obj_from_sample_name


def read_mutation_data(input_file: str, file_extension: str = "csv") -> pd.DataFrame:
    """
    Read mutation data, either in CSV or JSON format.
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


def process_mutation_df(df: pd.DataFrame, renaming_dict: dict = None) -> pd.DataFrame:
    """
    Process pd.DataFrame object, selecting specific columns and renaming then as required
    (maybe usefull for translations)
    """
    if renaming_dict is None and type(renaming_dict) != dict:
        renaming_dict = {
            "SAMPLE": "SAMPLE",
            "POS": "POS",
            "HGVS_P": "MUTATION",
            "AF": "AF",
            "EFFECT": "EFFECT",
            "GENE": "GENE",
            "LINEAGE": "LINEAGE",
        }

    # Rename and select columns
    df = df[renaming_dict.keys()]  # select specific keys
    df = df.rename(columns=renaming_dict)  # rename to the required output names

    return df


def generate_table(sample_name):
    # "B.1.1.7", "NC_045512"
    df = {}
    list_of_hgvs_p = []
    gene_list = []
    effect_list = []
    lineage_list = ["B.1.1.7", "B.1.1.7", "B.1.1.7", "B.1.1.7", "B.1.1.7"]
    sample_list = []
    chromosome = "NC_045512"
    sample_obj = get_sample_obj_from_sample_name(sample_name=sample_name)
    if sample_obj is not None:
        af = get_alelle_frequency_per_sample(
            sample_name=sample_name, chromosome=chromosome
        )
        pos = get_position_per_sample(sample_name=sample_name, chromosome=chromosome)
        variant_in_sample_objs = VariantInSample.objects.filter(sampleID_id=sample_obj)
        for variant_in_sample_obj in variant_in_sample_objs:
            variant_annotation_objs = VariantAnnotation.objects.filter(
                variantID_id=variant_in_sample_obj.get_variantID_id()
            )
            for variant_annotation_obj in variant_annotation_objs:
                hgvs_p = variant_annotation_obj.get_variant_in_sample_data()[1]
                list_of_hgvs_p.append(hgvs_p)

                geneID_id = variant_annotation_obj.get_geneID_id()
                gene_obj = Gene.objects.filter(gene_name__iexact=geneID_id).last()
                gene_list.append(gene_obj.get_gene_name())

                effect_obj = Effect.objects.filter(
                    effect__iexact=variant_annotation_obj.get_effectID_id()
                ).last()
                effect_list.append(effect_obj.get_effect())

                sample_list.append(sample_name)

        df["SAMPLE"] = sample_list
        df["POS"] = pos
        df["Mutation"] = list_of_hgvs_p
        df["AF"] = af
        df["EFFECT"] = effect_list
        df["GENE"] = gene_list
        df["LINEAGE"] = lineage_list

        return df
    else:
        return None


def create_mutation_table(sample):
    df = generate_table(sample_name=sample)
    df_pandas = pd.DataFrame.from_dict(df)
    PAGE_SIZE = 20

    app = DjangoDash("mutation_table")

    app.layout = html.Div(
        children=[
            html.P(id="mutation_table-message"),
            dcc.Dropdown(
                id="mutation_table-effect_dropdown",
                options=[{"label": i, "value": i} for i in df["EFFECT"]],
                clearable=False,
                multi=True,
                value=[{"label": i, "value": i} for i in df["EFFECT"]][0],
                style={"width": "400px"},
                placeholder="Mutation effect",
            ),
            html.Br(),
            dash_table.DataTable(
                id="mutation_datatable",
                data=df_pandas.to_dict("records"),
                columns=[{"name": i, "id": i} for i in df_pandas.columns],
                page_current=0,
                page_size=PAGE_SIZE,
                page_action="custom",
            ),
        ]
    )

    @app.callback(
        Output("mutation_datatable", "data"),
        Input("mutation_table-effect_dropdown", "value"),
    )
    def update_selected_effects(selected_effects):
        data = {}
        if type(selected_effects) == list and len(selected_effects) >= 1:
            data = df_pandas.to_dict("records")
        #   data = data[data["EFFECT"].isin(df["EFFECT"])]
        return data

    @app.callback(
        Output("mutation_table-message", "children"),
        Input("mutation_datatable", "active_cell"),
    )
    def show_clicks(active_cell):
        if active_cell:
            return str(active_cell)
        else:
            return "Click the table"

    # if __name__ == "__main__":
    #     app.run_server(debug=True)
