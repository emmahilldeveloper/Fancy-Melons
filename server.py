#This is fancy melons, an assignment for Hackbright Academy's 12-week software engineering bootcamp
from flask import Flask, redirect, render_template, session, request, flash, url_for, jsonify
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud
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


####### Log In #######
@app.route("/login", methods = ["GET", "POST"])
def login():
    """Return login page."""

    if request.method == "POST":
        email = request.form.get("email") #Get email from login form
        password = request.form.get("password") #Get password from login form
        user = crud.all_user_info_by_email(email) #Get all of user's data (from searching by entered email)
        session["user_id"] = user.user_id #Create session cookie for that user's information

        if user is None: #If the user is not in the database, ERROR
            flash("ERROR: Incorrect credentials. Try again.", category='danger')
            return redirect("/login")
        if user.password != password: #If the user's password is not equal to the saved password, ERROR
            flash("ERROR: Incorrect credentials. Try again.", category='danger')
            return redirect("/login")
        if user:
            return redirect("/profile")

    #Load the page
    else:
        return render_template("login.html")


####### Sign Up #######
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    """Return signup page."""

    if request.method == "POST":
        first_name = request.form.get("fname") #Get first name from signup form
        last_name = request.form.get("lname") #Get last name from signup form
        email = request.form.get("email") #Get email from signup form
        password = request.form.get("password") #Get password from signup form
        passwordconf = request.form.get("passwordconf") #Get password conf from signup form

        email_check = crud.all_user_info_by_email(email)
        if email_check:
            flash("Email already exists.", category='danger')
            return redirect("/login")
        
        if password != passwordconf:
            flash("Passwords do not match.", category='danger')

        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Successful.", category='success')
        return redirect("/profile")

    else:
        return render_template("signup.html")


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)