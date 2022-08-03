from dash.dependencies import Input, Output
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash


def create_gauge():
    app = DjangoDash("gauge_test")

    app.layout = html.Div(
        [
            daq.Gauge(id="my-gauge-1", label="Default", value=6),
            dcc.Slider(id="my-gauge-slider-1", min=0, max=10, step=1, value=5),
        ]
    )

    @app.callback(Output("my-gauge-1", "value"), Input("my-gauge-slider-1", "value"))
    def update_output(value):
        return value
