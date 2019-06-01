"""Main flask app."""

import os

import pandas as pd
import dotenv
import pytz

# flask imports
from flask import Flask
from flask import render_template

# flask extensions
from flask_sqlalchemy import SQLAlchemy

# library imports
from . import plotting

if os.path.exists(".env"):
    dotenv.load_dotenv(dotenv_path=".env")
elif os.path.exists("../.env"):
    dotenv.load_dotenv(dotenv_path="../.env")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


@app.route("/health")
def health():
    """Health check."""
    return "ok"


@app.route("/")
def mainpage():
    """Render the main page."""
    # sql query
    sql = """
    select 
      convert_tz(dttm_utc, 'UTC', 'US/Eastern') as dttm_nyc
    , ping_ms
    , download_mbits
    , upload_mbits
    from snapshots
    where dttm_utc >= (curdate() + interval -90 day)
    order by 1 desc
    """

    # grab the dataframe and localize the datetime to nyc
    df = pd.read_sql_query(sql, db.engine).assign(
        dttm_nyc=lambda df: df.dttm_nyc.apply(pytz.timezone("US/Eastern").localize)
    )

    charts = []
    charts.append(plotting.timeseries(df, "ping_ms"))
    charts.append(plotting.timeseries(df, "download_mbits"))
    charts.append(plotting.timeseries(df, "upload_mbits"))
    return render_template("main.html", charts=charts)
