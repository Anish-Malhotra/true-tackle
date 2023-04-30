from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_pyfile('db_config.py')
CORS(app)

db = SQLAlchemy(app)
