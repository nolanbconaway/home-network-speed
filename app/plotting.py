"""Functions to create plots given data."""
import datetime
import pandas as pd
from palettable.cartocolors.qualitative import Safe_7

weekday_names = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


def _hour_to_time(num: int):
    """Convert an hour number to a time string."""
    return datetime.datetime.now().replace(hour=num).strftime("%-I %p")


def _rgb_to_string(rgb_tup: tuple, alpha: int = 1) -> str:
    """Convert a RGB tuple to a string for chart js."""
    return f"rgba({', '.join(map(str, rgb_tup))}, {alpha})"


def timeseries(
    df: pd.DataFrame, var: str, dataset_kws: dict = dict(), options_kws: dict = dict()
) -> dict:
    """Make the full timeseries plot for a given variable."""
    # get tuples of data
    data = [dict(x=row["date_formatted"], y=row[var]) for i, row in df.iterrows()]

    # make datasets
    _dataset_kws = {
        "data": data,
        "label": var,
        "fill": False,
        "borderColor": "black",
        "pointRadius": 0,
        "borderWidth": 2,
    }
    _dataset_kws.update(dataset_kws)

    # get options
    options = {
        "responsive": True,
        "scales": {"xAxes": [{"type": "time", "tooltipFormat": "LT"}]},
        "legend": {"display": False},
        "title": {"display": True, "text": var},
    }
    options.update(options_kws)

    return {"type": "line", "data": {"datasets": [_dataset_kws]}, "options": options}


def hour_distributions(
    df: pd.DataFrame, var: str, dataset_kws: dict = dict(), options_kws: dict = dict()
) -> dict:

    avgs = (
        df.assign(dow=lambda x: x.dttm_nyc.dt.weekday, hod=lambda x: x.dttm_nyc.dt.hour)
        .groupby(["dow", "hod"])[var]
        .mean()
        .reset_index()
        .sort_values(["dow", "hod"])
    )

    # make datasets
    _dataset_kws = {}
    _dataset_kws.update(dataset_kws)
    datasets = []
    for dow, weekday_name in weekday_names.items():
        rows = avgs.loc[lambda x: x.dow == dow]
        print(_rgb_to_string(Safe_7.colors[dow], alpha=255 / 7))
        datasets.append(
            {
                "label": weekday_name,
                "data": rows[var].tolist(),
                "backgroundColor": _rgb_to_string(Safe_7.colors[dow], alpha=1 / 4),
                "pointRadius": 0,
                **_dataset_kws,
            }
        )

    # make options
    options = {"responsive": True, "title": {"display": True, "text": var}}
    options.update(options_kws)

    return {
        "type": "radar",
        "data": {"labels": list(map(_hour_to_time, range(24))), "datasets": datasets},
        "options": options,
    }

