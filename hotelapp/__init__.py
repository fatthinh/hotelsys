from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '890f32ff363679f635988bd8c7910afe41fb463937feafb39df5490489c4c171'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/bookingdb?charset=utf8mb4" % quote(
    '0335037042Think.')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8


db = SQLAlchemy(app)
