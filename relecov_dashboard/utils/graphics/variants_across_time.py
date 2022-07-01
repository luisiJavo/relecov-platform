"""
Filled Area Plots for VOC, VOI, lineages
Right now it is set up for lineages
"""

# Dash libs
import dash

from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# Other libs
import pandas as pd
import json
import datetime


def merge_data(bioinfo_metadata_file, metadata_lab_file) -> pd.DataFrame:
    """
    Merge bioinformatics metadata with lab metadata and
    output a dataframe with the following columns:
    - "sequencing_sample_id"
    - "lineage_name"
    - "collecting_institution"
    - "collection_device"
    - "flowcell_kit"
    - "geo_loc_city"
    - "geo_loc_state"
    - "geo_loc_country"
    - "geo_loc_latitude"
    - "geo_loc_longitude"
    - "purpose_sampling"
    - "sample_collection_date"
    - "sample_received_date"
    - "sequencing_date"
    """
    with open(bioinfo_metadata_file) as f:
        # JSON must have a "primary key", which is the sample ID
        # Sample data
        bioinfo_metadata_df = pd.DataFrame.from_dict(json.load(f), orient="index")
        bioinfo_metadata_df = bioinfo_metadata_df.reset_index().rename(
            columns={"index": "sequencing_sample_id"}
        )

    with open(metadata_lab_file) as f:
        # Lab metadata
        metadata_lab_df = pd.DataFrame.from_dict(json.load(f), orient="columns")

    # Select columns
    bioinfo_metadata_df = bioinfo_metadata_df[["sequencing_sample_id", "lineage_name"]]

    metadata_lab_df = metadata_lab_df[
        [
            "sequencing_sample_id",
            "collecting_institution",
            "collection_device",
            "flowcell_kit",
            "geo_loc_city",
            "geo_loc_state",
            "geo_loc_country",
            "geo_loc_latitude",
            "geo_loc_longitude",
            "purpose_sampling",
            "sample_collection_date",
            "sample_received_date",
            "sequencing_date",
        ]
    ]

    # Merge
    bioinfo_metadata_df["sequencing_sample_id"] = bioinfo_metadata_df[
        "sequencing_sample_id"
    ].astype(int)
    metadata_lab_df["sequencing_sample_id"] = metadata_lab_df[
        "sequencing_sample_id"
    ].astype(int)
    merged_df = pd.merge(
        bioinfo_metadata_df,
        metadata_lab_df,
        left_on="sequencing_sample_id",
        right_on="sequencing_sample_id",
    )

    return merged_df


def get_proportions(
    df: pd.DataFrame, date_col: str, target_col: str, date_range: list
) -> pd.DataFrame:
    """
    Calculate proportions of an element in each date
    The function receives a dataframe with columns:
    - date_col | Ex: sample_collection_date
    - target_col | Ex: lineage_name
    It then counts the proportion of the target_col in each date. For example, if
    target_col is lineage_name, it will count how many times each lineage appears in each
    day and then calculate the proportion over 100
    Input:
    - df
    - date_col - ex: "sample_collection_date"
    - target_col - ex: "lineage_name"
    - date_range - ex: [datetime.date(2022,1,1),datetime.date(2022,2,1)]
    """
    # Filter dates
    if date_range:
        df[date_col] = pd.to_datetime(df[date_col]).dt.date
        df = df[(df[date_col] >= date_range[0]) & (df[date_col] <= date_range[1])]

    # Filter columns
    df = df[[target_col, date_col]]

    # Calculate counts of lineage per date
    lineage_counts = df.value_counts().reset_index()
    lineage_counts.columns = [target_col, date_col, "count"]

    # For each date, calculate the proportion of each lineage in range 0,100
    dates = list(lineage_counts[date_col].unique())
    df_list = []
    for date in dates:
        tmp = lineage_counts[lineage_counts[date_col] == date].copy()
        tmp["proportion"] = 100 * tmp["count"] / tmp["count"].sum()
        df_list.append(tmp)

    lineage_proportions = pd.concat(df_list)
    lineage_proportions["proportion"] = lineage_proportions["proportion"].round(2)

    return lineage_proportions


def get_stacked_area_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str,
    xlabel: str = None,
    ylabel: str = None,
    **kwargs
) -> px.area:
    """
    Get a stacked plotly.express.area plot
    Column X should represent a timeline and Y the porportion of an element (scale 0,100)
    """
    fig = px.area(
        df,
        x=x,
        y=y,
        color=color,
        line_group=color,
    )
    fig.update_layout(yaxis_range=(0, 100))
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(
        hovermode="x unified",
        xaxis={"title": xlabel if xlabel else x},
        yaxis={"title": ylabel if ylabel else y},
    )

    return fig


def create_lineage_evolution(df: pd.DataFrame, date_range: list) -> dash.Dash:
    """
    Create Dash app to plot a stacked area plotly chart, with
    dates in the X axis and proportions of lineages in axis Y, using lineages
    as colors
    """

    def get_data(df, date_range):
        lineage_proportions = get_proportions(
            df,
            date_col="sample_collection_date",
            target_col="lineage_name",
            date_range=date_range,
        )
        return lineage_proportions

    def get_fig(df):
        fig = get_stacked_area_plot(
            df,
            x="sample_collection_date",
            y="proportion",
            color="lineage_name",
            xlabel="Date",
            ylabel="Proportion",
        )
        return fig

    lineage_proportions = get_data(df, date_range)

    # ---- Dash app ----
    app = dash.Dash(__name__)

    app.layout = html.Div(
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "justify-content": "start",
                    "align-items": "flex-start",
                },
                children=[
                    dcc.DatePickerRange(
                        id="lineage_area-select_dates",
                        start_date=date_range[0],
                        end_date=date_range[1],
                    ),
                ],
            ),
            dcc.Graph(
                id="lineage_area",
                figure=get_fig(lineage_proportions),
                style={"width": "1500px", "height": "700px"},
            ),
        ]
    )

    def update_selected_dates(data: pd.DataFrame, selected_sample: int):
        if selected_sample and type(selected_sample) == int:
            data = data[data["SAMPLE"].isin([selected_sample])]
        return data

    @app.callback(
        Output("lineage_area", "figure"),
        Input("lineage_area-select_dates", "start_date"),
        Input("lineage_area-select_dates", "end_date"),
    )
    def update_graph(start_date: datetime.date, end_date: datetime.date):
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        if start_date and end_date:
            date_range = [start_date, end_date]
        else:
            date_range = None

        tmp = get_data(df, date_range=date_range)
        fig = get_fig(tmp)
        return fig

    return app


if __name__ == "__main__":
    # Input
    bioinfo_metadata_file = (
        "/home/usuario/Proyectos/relecov/relecov-platform/data/bioinfo_metadata.json"
    )
    metadata_lab_file = "/home/usuario/Proyectos/relecov/relecov-platform/data/processed_metadata_lab_20220208_20220613.json"
    date_range = [datetime.date(2022, 1, 1), datetime.date(2022, 2, 1)]

    # Get data
    merged_df = merge_data(bioinfo_metadata_file, metadata_lab_file)

    # App
    app = create_lineage_evolution(merged_df, date_range)
    app.run_server(debug=True)
