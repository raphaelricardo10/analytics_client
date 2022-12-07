from plots.plot import Plot
import plotly.express as px
import plotly.graph_objects as go
class TemperaturePlot(Plot):
    def figure(self, df) -> go.Figure:
        figs = self.plot_all_devices(df)

        return self.join_plots(figs)

    def plot_all_devices(self, df):
        figs = []
        devices = df.device.unique()

        for device in devices:
            df_by_device = df[df.device == device]
            figs.append(px.line(df_by_device, x="ts", y="temp"))

        return figs

    @staticmethod
    def join_plots(figs):
        combined_figs = figs[0].data
        for figure in figs[1:]:
            combined_figs += figure.data

        return go.Figure(data=combined_figs)