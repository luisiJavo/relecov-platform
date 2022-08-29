from plotly.offline import plot

# import plotly.graph_objects as go
import plotly.express as px


def histogram_graphic(d_frame, option):
    graphs = []
    graphs.append(
        px.histogram(
            d_frame,
            x="total_bill",
            y="tip",
            color="sex",
            marginal="rug",
            hover_data=d_frame.columns,
        )
    )

    # Setting layout of the figure.
    layout = {
        "title": option["title"],
        "xaxis_title": option["x_axis"],
        "yaxis_title": option["y_axis"],
        "height": option["height"],
        "width": option["width"],
    }

    # Getting HTML needed to render the plot.
    plot_div = plot({"data": graphs, "layout": layout}, output_type="div")
    return plot_div


def pie_graphic(d_frame, option):
    return
