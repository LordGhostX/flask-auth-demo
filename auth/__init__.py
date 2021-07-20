from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SERIALIZER_TOKEN"] = "SERIALIZER_TOKEN"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///auth-demo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
