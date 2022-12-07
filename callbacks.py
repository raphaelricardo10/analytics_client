import os
import pandas as pd

from app import app
from dash import Output, Input, State, no_update

from decoders import decode_dataframe
from bigquery_client import BigQueryClient
from plots.temperature_plot import TemperaturePlot

temperature_plot = TemperaturePlot()

bq_client = BigQueryClient(
    project_id=os.getenv("PROJECT_ID"), dataset=os.getenv("BQ_DATASET")
)


@app.callback(
    Output(component_id="df", component_property="data"),
    Output(component_id='df_start_date', component_property='data'),
    State(component_id="df", component_property="data"),
    State(component_id='df_start_date', component_property='data'),
    Input(component_id="interval-component", component_property="n_intervals"),
)
def update_df(df, start_date, _):
    df = decode_dataframe(df)
    
    new_df = bq_client.select(
        "multisensor_data", start_date=start_date, to_df=True
    ).drop_duplicates()

    start_date = new_df.ts.max()

    if df is None:
        return new_df.to_json(), start_date
        
    df = pd.concat([df, new_df], join="inner", ignore_index=True)

    return df.to_json(), start_date


@app.callback(
    Output(component_id="temperature-plot", component_property="figure"),
    Input(component_id="df", component_property="data"),
)
def update_temperature_plot(df):
    if df is None:
        return no_update

    df = decode_dataframe(df)
    return temperature_plot.figure(df)
