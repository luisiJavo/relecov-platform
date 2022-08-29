# import os
import pandas as pd

# from django.conf import settings
from django_plotly_dash import DjangoDash
import dash_table
from dash.dependencies import Input, Output

import dash_bio as dashbio
import dash_html_components as html
# from dash import html
from dash_bio.utils import PdbParser, create_mol3d_style


def create_molecule3D_graph():
    app = DjangoDash("model3D")

    parser = PdbParser("https://git.io/4K8X.pdb")
    """
    parser = PdbParser(os.path.join(
            settings.BASE_DIR, "relecov_dashboard", "utils", "pdb_files", "6vxx.pdb"
        ))
    """

    data = parser.mol3d_data()
    styles = create_mol3d_style(
        data["atoms"], visualization_type="cartoon", color_element="residue"
    )

    app.layout = html.Div(
        [
            dashbio.Molecule3dViewer(
                width="auto",
                id="dashbio-default-molecule3d",
                modelData=data,
                styles=styles,
                labels=[
                    {
                        "text": "Residue Name: GLY1",
                        "fontColor": "red",
                        "font": "Courier New, monospace",
                    },
                    {
                        "text": "Residue Chain: A",
                        "position": {"x": 15.407, "y": -8.432, "z": 6.573},
                    },
                ],
            ),
            "Selection data",
            html.Hr(),
            html.Div(id="default-molecule3d-output"),
        ]
    )

    @app.callback(
        Output("default-molecule3d-output", "children"),
        Input("dashbio-default-molecule3d", "selectedAtomIds"),
    )
    def show_selected_atoms(atom_ids):
        if atom_ids is None or len(atom_ids) == 0:
            return "No atom has been selected. Click somewhere on the molecular \
            structure to select an atom."
        return [
            html.Div(
                [
                    html.Div("Element: {}".format(data["atoms"][atm]["elem"])),
                    html.Div("Chain: {}".format(data["atoms"][atm]["chain"])),
                    html.Div(
                        "Residue name: {}".format(data["atoms"][atm]["residue_name"])
                    ),
                    html.Br(),
                ]
            )
            for atm in atom_ids
        ]


def create_molecule3D_zoom_specific_residues():
    app = DjangoDash("model3D_zoom_residues")

    parser = PdbParser("https://git.io/4K8X.pdb")

    data = parser.mol3d_data()
    styles = create_mol3d_style(
        data["atoms"], visualization_type="cartoon", color_element="residue"
    )

    df = pd.DataFrame(data["atoms"])
    df = df.drop_duplicates(subset=["residue_name"])
    df["positions"] = df["positions"].apply(lambda x: ", ".join(map(str, x)))

    app.layout = html.Div(
        [
            dash_table.DataTable(
                id="zooming-specific-residue-table",
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                row_selectable="single",
                page_size=10,
            ),
            dashbio.Molecule3dViewer(
                id="zooming-specific-molecule3d-zoomto", modelData=data, styles=styles
            ),
        ]
    )

    @app.callback(
        Output("zooming-specific-molecule3d-zoomto", "zoomTo"),
        Output("zooming-specific-molecule3d-zoomto", "labels"),
        Input("zooming-specific-residue-table", "selected_rows"),
        prevent_initial_call=True,
    )
    def residue(selected_row):
        row = df.iloc[selected_row]
        row["positions"] = row["positions"].apply(
            lambda x: [float(x) for x in x.split(",")]
        )
        return [
            {
                "sel": {"chain": row["chain"], "resi": row["residue_index"]},
                "animationDuration": 1500,
                "fixedPath": True,
            },
            [
                {
                    "text": "Residue Name: {}".format(row["residue_name"].values[0]),
                    "position": {
                        "x": row["positions"].values[0][0],
                        "y": row["positions"].values[0][1],
                        "z": row["positions"].values[0][2],
                    },
                }
            ],
        ]


def create_molecule3D_labels():
    parser = PdbParser("https://git.io/4K8X.pdb")

    data = parser.mol3d_data()
    styles = create_mol3d_style(
        data["atoms"], visualization_type="cartoon", color_element="residue"
    )

    dashbio.Molecule3dViewer(
        modelData=data,
        styles=styles,
        labels=[
            {
                "text": "Residue Name: GLY1",
                "fontColor": "red",
                "font": "Courier New, monospace",
            },
            {
                "text": "Residue Chain: A",
                "position": {"x": 15.407, "y": -8.432, "z": 6.573},
            },
        ],
    )
