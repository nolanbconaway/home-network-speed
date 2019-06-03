"""Functions to create plots given data."""
import datetime
import pandas as pd
from palettable.cartocolors.qualitative import Safe_2


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
        "maintainAspectRatio": True,
        "scales": {
            "xAxes": [{"type": "time", "tooltipFormat": "LT"}],
            "yAxes": [{"type": "linear", "ticks": {"min": 0}}],
        },
        "legend": {"display": False},
        "title": {"display": True, "text": var},
    }
    options.update(options_kws)

    return {"type": "line", "data": {"datasets": [_dataset_kws]}, "options": options}


def hour_distributions(
    df: pd.DataFrame, var: str, dataset_kws: dict = dict(), options_kws: dict = dict()
) -> dict:
    """Make radar charts showing hourly averages."""
    avgs = (
        df.assign(
            is_weekday=lambda x: x.dttm_nyc.dt.weekday < 4,
            hod=lambda x: x.dttm_nyc.dt.hour,
        )
        .groupby(["is_weekday", "hod"])[var]
        .mean()
        .reset_index()
        .sort_values(["is_weekday", "hod"])
    )

    # make datasets
    _dataset_kws = {}
    _dataset_kws.update(dataset_kws)
    datasets = []
    for is_weekday in (True, False):
        rows = avgs.loc[lambda x: x.is_weekday == is_weekday]
        datasets.append(
            {
                "label": "Weekday" if is_weekday else "Weekend",
                "data": rows[var].tolist(),
                "backgroundColor": _rgb_to_string(
                    Safe_2.colors[is_weekday], alpha=1 / 2
                ),
                "pointRadius": 0,
                **_dataset_kws,
            }
        )

    # make options
    options = {
        "responsive": True,
        "maintainAspectRatio": True,
        "title": {"display": True, "text": var},
        "scale": {"ticks": {"beginAtZero": True}},
        "legend": {"position": "right"},
    }
    options.update(options_kws)

    return {
        "type": "radar",
        "data": {"labels": list(map(_hour_to_time, range(24))), "datasets": datasets},
        "options": options,
    }

