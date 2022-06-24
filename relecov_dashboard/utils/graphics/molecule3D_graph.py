from django_plotly_dash import DjangoDash
from dash.dependencies import Input, Output

import dash_bio as dashbio
import dash_html_components as html
from dash_bio.utils import PdbParser, create_mol3d_style


def create_molecule3D_graph():
    app = DjangoDash("model3D")

    parser = PdbParser("https://git.io/4K8X.pdb")

    data = parser.mol3d_data()
    styles = create_mol3d_style(
        data["atoms"], visualization_type="cartoon", color_element="residue"
    )

    app.layout = html.Div(
        [
            dashbio.Molecule3dViewer(
                width="1200",
                id="dashbio-default-molecule3d",
                modelData=data,
                styles=styles,
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
