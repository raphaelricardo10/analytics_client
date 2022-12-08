import pandas as pd
from plots.plot import Plot
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class TemperaturePlot(Plot):
    @staticmethod
    def figure(df: pd.DataFrame) -> go.Figure:

        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            showlegend=True,
            title="Temperature in last hour",
            xaxis_title="Time",
            yaxis_title="Temperature (°F)",
            legend_title="Device MAC address",
        )

        for df in TemperaturePlot.get_dfs_by_device(df):
            fig.add_trace(
                go.Scatter(x=df.ts, y=df.temp, name=df.device.iloc[0]),
            )

        return fig

    @staticmethod
    def get_dfs_by_device(df: pd.DataFrame):
        dfs_by_device = []
        devices = df.device.unique()

        for device in devices:
            dfs_by_device.append(df[df.device == device])

        return dfs_by_device


class LastHourTemperaturePlot(TemperaturePlot):
    def figure(df: pd.DataFrame):

        return TemperaturePlot.figure(Plot._filter_last_hour(df))
