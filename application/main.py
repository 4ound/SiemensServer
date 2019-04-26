from flask import Flask
from application.models import *
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_STRING')
db.init_app(app)
