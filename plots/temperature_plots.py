import pandas as pd
from plots.plot import Plot
import plotly.express as px
import plotly.graph_objects as go


class TemperaturePlot(Plot):
    @staticmethod
    def figure(df: pd.DataFrame) -> go.Figure:
        figs = TemperaturePlot.plot_all_devices(df)

        return TemperaturePlot.join_plots(figs)

    @staticmethod
    def plot_all_devices(df: pd.DataFrame):
        figs = []
        devices = df.device.unique()

        for device in devices:
            df_by_device = df[df.device == device]
            figs.append(px.line(df_by_device, x="ts", y="temp"))

        return figs

    @staticmethod
    def join_plots(figs: "list[go.Figure]") -> go.Figure:
        combined_figs = figs[0].data
        for figure in figs[1:]:
            combined_figs += figure.data

        return go.Figure(data=combined_figs)


class LastHourTemperaturePlot(TemperaturePlot):
    def figure(df: pd.DataFrame):

        return TemperaturePlot.figure(Plot._filter_last_hour(df))
