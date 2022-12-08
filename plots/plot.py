import pandas as pd
import plotly.graph_objects as go
from datetime import timedelta
from abc import ABC, abstractstaticmethod


class Plot(ABC):
    def __init__(self) -> None:
        raise ValueError("This class is static!")

    @abstractstaticmethod
    def figure(df: pd.DataFrame) -> go.Figure:
        pass

    @staticmethod
    def empty_plot() -> go.Figure:
        return go.Figure(data=[go.Scatter(x=[], y=[])])

    @staticmethod
    def _basic_figure() -> go.Figure:
        pass

    @staticmethod
    def _filter_last_hour(
        df: pd.DataFrame,
    ):
        one_hour_ago = df.ts.max() - timedelta(hours=1)
        
        return df[df.ts >= one_hour_ago]
