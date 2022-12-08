import os
import pandas as pd

import diskcache
from datetime import datetime, timedelta
from dash.long_callback import DiskcacheLongCallbackManager

from sys import platform

from app import app
from dash import Output, Input, State, no_update

from decoders import decode_dataframe
from bigquery_client import BigQueryClient
from plots.temperature_plots import LastHourTemperaturePlot

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

bq_client = BigQueryClient(
    project_id=os.getenv("PROJECT_ID"), dataset=os.getenv("BQ_DATASET")
)

dynamic_callback = app.callback if platform == 'darwin' else app.long_callback

@dynamic_callback(
    Output(component_id="df", component_property="data"),
    Output(component_id="df_start_date", component_property="data"),
    State(component_id="df", component_property="data"),
    State(component_id="df_start_date", component_property="data"),
    Input(component_id="interval-component", component_property="n_intervals"),
    manager=long_callback_manager,
)
def update_df(df, start_date, _):
    df = decode_dataframe(df)
    limit = 500 if df is not None else None

    new_df = bq_client.select(
        os.getenv('BQ_TABLE'), start_date=start_date, to_df=True, limit=limit
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
    return LastHourTemperaturePlot.figure(df)


@app.callback(
    Output(component_id="interval-component", component_property="interval"),
    Input(component_id="interval-component", component_property="n_intervals"),
)
def update_interval(num_intervals):
    if num_intervals > 0:
        return 3*1000

    return no_update

