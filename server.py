#This is fancy melons, an assignment for Hackbright Academy's 12-week software engineering bootcamp
from flask import Flask, redirect, render_template, session, request, flash, url_for, jsonify
from jinja2 import StrictUndefined
import urllib.parse
import requests
import os
from datetime import datetime

app = Flask(__name__)
app.config.update(TESTING=True, SECRET_KEY='DEV')
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

####### Home #######

@app.route("/")
def index():
    """Return homepage."""
    return render_template("homepage.html")

@app.route("/login")
def login():
    """Return login page."""
    return render_template("login.html")





if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)