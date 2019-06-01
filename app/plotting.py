"""Functions to create plots given data."""
import pandas as pd
import pytz


def timeseries(df: pd.DataFrame, var: str) -> dict:
    """Make the full timeseries plot for a given variable."""
    data = [dict(x=row["dttm_nyc"], y=row[var]) for i, row in df.iterrows()]
    print(data[0])
    return {
        "type": "line",
        "data": {"datasets": [{"data": data, "label": var}]},
        "options": {"responsive": True, "scales": {"xAxes": [{"type": "time"}]}},
    }
