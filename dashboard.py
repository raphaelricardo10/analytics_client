from app import app
from dash import html, dcc

from plots.plot import Plot

app.layout = html.Div(children=[
    dcc.Store('df'),
    dcc.Store('df_start_date', data=None),
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    dcc.Graph(
        id='temperature-plot',
        figure=Plot.empty_plot()
    ),
    dcc.Interval(
        id='interval-component',
        interval=10*1000, # in milliseconds
        n_intervals=0,
    )
])