from dash.dependencies import Input, Output
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
from django_plotly_dash import DjangoDash

import plotly.graph_objects as go


def create_gauge():
    app = DjangoDash("gauge_test")

    app.layout = html.Div(
        [
            daq.Gauge(id="my-gauge-1", label="Received Samples", value=96),
            # dcc.Slider(id="my-gauge-slider-1", min=0, max=10, step=1, value=5),
        ]
    )
    """
    @app.callback(Output("my-gauge-1", "value"), Input("my-gauge-slider-1", "value"))
    def update_output(value):
        return value
    """


def create_medium_gauge():
    app = DjangoDash("gauge_medium")
    app.layout = html.Div(
        fig=go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=270,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Speed"},
            )
        )
    )
    fig.update_layout(transition_duration=500)

    return fig
