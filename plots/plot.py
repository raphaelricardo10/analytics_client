import plotly.graph_objects as go
from abc import ABC, abstractmethod


class Plot(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def figure(self, df: None) -> go.Figure:
        pass

    @staticmethod
    def empty_plot():
        return go.Figure(data=[go.Scatter(x=[], y=[])])