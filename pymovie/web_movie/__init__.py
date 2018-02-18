from flask import Flask
from ..model import SESSION

app = Flask(__name__)
app.config.from_object('config')

# DB setting
session = SESSION()
