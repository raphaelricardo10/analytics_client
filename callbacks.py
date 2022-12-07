import os

from app import app
from dash import Output, Input

from bigquery_client import BigQueryClient
from plots.temperature_plot import TemperaturePlot

temperature_plot = TemperaturePlot()

bq_client = BigQueryClient(
    project_id=os.getenv("PROJECT_ID"), dataset=os.getenv("BQ_DATASET")
)


@app.callback(
    Output(component_id="df", component_property="data"),
    Input(component_id="interval-component", component_property="n_intervals"),
)
def update_df(df):
    return (
        bq_client.select("multisensor_data", to_df=True)
        .drop_duplicates()
        .to_json()
    )


@app.callback(
    Output(component_id="temperature-plot", component_property="figure"),
    Input(component_id="df", component_property="data"),
)
def update_temperature_plot(df):
    return temperature_plot.figure(df)
