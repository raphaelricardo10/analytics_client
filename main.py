import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dotenv import load_dotenv
from dash import Dash, html, dcc
from bigquery_client import BigQueryClient

load_dotenv()

bq_client = BigQueryClient(project_id=os.getenv('PROJECT_ID'), dataset=os.getenv('BQ_DATASET'))

df = bq_client.select('multisensor_data', to_df=True).drop_duplicates()

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

fig = px.line(df, x="ts", y="temp")

devices = df['device'].unique()

def plot_by_device():
    devices = df['device'].unique()
    figs = []

    for device in devices:
        df_by_device = df[df.device == device]
        figs.append(px.line(df_by_device, x="ts", y="temp"))

    combined_figs = figs[0].data
    for figure in figs[1:]:
        combined_figs += figure.data

    return go.Figure(data=combined_figs)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Graph(
        id='example-graph',
        figure=plot_by_device()
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)