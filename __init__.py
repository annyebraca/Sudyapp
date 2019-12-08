"""
The flask.
"""

from flask import Flask

app = Flask(__name__)

from theapp import views
