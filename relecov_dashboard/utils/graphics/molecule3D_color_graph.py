import pandas as pd

from django_plotly_dash import DjangoDash
import dash_table
from dash.dependencies import Input, Output

import dash_bio as dashbio
import dash_html_components as html
from dash_bio.utils import PdbParser, create_mol3d_style
from relecov_dashboard.utils.graphics.graphics_handling import (
    screen_size,
    set_screen_size
)


def create_molecule3D_zoom_specific_residues():
    size =set_screen_size(screen_size())
    
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
            html.P("Data table"),
            dash_table.DataTable(
                id="zooming-specific-residue-table",
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                row_selectable="single",
                page_size=10,
            ),
            html.Br(),
            html.Br(),
            html.Hr(),
            html.P("Molecule 3D Viewer"),
            html.Div(
                children=[
                    dashbio.Molecule3dViewer(
                        id="zooming-specific-molecule3d-zoomto",
                        modelData=data,
                        styles=styles,
                        height=size[1],
                        width=size[0],
                        zoom={ "factor": 1.2, "animationDuration": 0, "fixedPath": False,}
                    ),
                ],
                style={
                    "display": "inline-flex",
                    "justify-content": "center",
                    "align-self": "auto",
                },
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
