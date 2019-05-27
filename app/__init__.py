import os
from flask import Flask

# flask extensions
from flask_sqlalchemy import SQLAlchemy

# load dotenv
import dotenv

if os.path.exists(".env"):
    dotenv.load_dotenv(dotenv_path=".env")
elif os.path.exists("../.env"):
    dotenv.load_dotenv(dotenv_path="../.env")


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
