from app import app
from dash import html, dcc

from plots.plot import Plot

app.layout = html.Div(
    children=[
        dcc.Store("df"),
        dcc.Store("df_start_date", data=None),
        html.Div(
            className='titles-container',
            children=[
                html.H1(
                    children="Real-time monitoring dashboard", className="page-title"
                ),
                html.H2(
                    children="Easily keep track of sensors no matter where they are",
                    className="page-subtitle",
                ),
            ]
        ),
        dcc.Graph(
            id="temperature-plot", figure=Plot.empty_plot(), className="temp-plot-hour"
        ),
        dcc.Interval(
            id="interval-component",
            interval=10 * 1000,  # in milliseconds
            n_intervals=0,
        ),
    ]
)
