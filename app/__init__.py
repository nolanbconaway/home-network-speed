"""Main flask app."""
import os

import dotenv
import pandas as pd
import pytz

# flask imports
from flask import Flask, render_template

# flask extensions
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

# library imports
from . import plotting

if os.path.exists(".env"):
    dotenv.load_dotenv(dotenv_path=".env")
elif os.path.exists("../.env"):
    dotenv.load_dotenv(dotenv_path="../.env")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app=app)
limiter = Limiter(app, key_func=get_remote_address, storage_uri="memory://")
mysql_limit = limiter.shared_limit(["60 per hour", "120 per day"], scope="mysql")


@app.route("/health")
def health():
    """Health check."""
    return "ok"


@app.route("/today")
@mysql_limit
def today():
    """Render the main page."""
    # sql query
    sql = """
    select 
      convert_tz(dttm_utc, 'UTC', 'US/Eastern') as dttm_nyc
    , ping_ms as 'Ping (ms)'
    , download_mbits as 'Download (mbits)'
    , upload_mbits as 'Upload (mbits)'
    from snapshots
    where dttm_utc >= (UTC_TIMESTAMP() + interval -1440 minute)
    order by 1 desc
    """

    df = (
        pd.read_sql_query(sql, db.session.connection())
        # make datetime tz aware
        .assign(
            dttm_nyc=lambda df: df.dttm_nyc.apply(pytz.timezone("US/Eastern").localize)
        )
        # make a formatted version for ease of use with chart js
        .assign(date_formatted=lambda x: x.dttm_nyc.dt.strftime("%Y-%m-%d %H:%M:%S"))
    )

    charts = []
    charts.append(plotting.timeseries(df, "Ping (ms)"))
    charts.append(plotting.timeseries(df, "Download (mbits)"))
    charts.append(plotting.timeseries(df, "Upload (mbits)"))
    return render_template("display_charts.html", charts=charts)


@app.route("/hourly")
@mysql_limit
def hourly():
    """Render the main page."""
    # sql query
    sql = """
    select 
      convert_tz(dttm_utc, 'UTC', 'US/Eastern') as dttm_nyc
    , ping_ms as 'Ping (ms)'
    , download_mbits as 'Download (mbits)'
    , upload_mbits as 'Upload (mbits)'
    from snapshots
    where dttm_utc >= (UTC_TIMESTAMP() + interval -30 day)
    order by 1 desc
    """

    df = (
        pd.read_sql_query(sql, db.session.connection())
        # make datetime tz aware
        .assign(
            dttm_nyc=lambda df: df.dttm_nyc.apply(pytz.timezone("US/Eastern").localize)
        )
        # make a formatted version for ease of use with chart js
        .assign(date_formatted=lambda x: x.dttm_nyc.dt.strftime("%Y-%m-%d %H:%M:%S"))
    )

    charts = []
    charts.append(plotting.hour_distributions(df, "Ping (ms)"))
    charts.append(plotting.hour_distributions(df, "Download (mbits)"))
    charts.append(plotting.hour_distributions(df, "Upload (mbits)"))
    return render_template("display_charts.html", charts=charts)


@app.route("/")
@mysql_limit
def about():
    """Show the about page."""
    sql = """
    select
    convert_tz(dttm_utc, 'UTC', 'US/Eastern') as dttm_nyc,
    ping_ms                                   as 'Ping (ms)',
    download_mbits                            as 'Download (mbits)',
    upload_mbits                              as 'Upload (mbits)'
    from snapshots
    order by dttm_utc desc
    limit 1
    """

    keys = ("dttm_nyc", "Ping (ms)", "Download (mbits)", "Upload (mbits)")
    record = dict(zip(keys, db.session.execute(sql).fetchone()))
    return render_template("about.html", last_snapshot=record)
