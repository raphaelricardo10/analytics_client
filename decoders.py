import pandas as pd
from dash.exceptions import PreventUpdate

def decode_dataframe(df):
    if df is None:
        return None

    df = pd.read_json(df)
    df.ts = pd.to_datetime(df.ts, unit='ms')

    return df