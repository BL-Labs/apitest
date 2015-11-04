
from models import *
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, send_file, jsonify, make_response, current_app, Flask

import tempfile

from random import randint

import json

from datetime import timedelta
from functools import update_wrapper

from apihelpers import *

# app-wide configuration
DEBUG = True

# create our app and load in the config
app = Flask(__name__)
app.config.from_object(__name__)


@app.errorhandler(404)
def page_not_found(error):
  return render_template("404.html"), 404

@app.route("/", methods=['GET', 'POST'])
def home_page():
  return render_template('home_page.html')

