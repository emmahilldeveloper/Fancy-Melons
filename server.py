#This is Fancy Melons, an assignment for Hackbright Academy's 12-week software engineering bootcamp
from flask import Flask, redirect, render_template, session, request, flash, url_for, jsonify
from jinja2 import StrictUndefined
from model import connect_to_db, db
import crud
import urllib.parse
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.update(TESTING=True, SECRET_KEY='DEV')
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True





####### Home #######
@app.route("/")
def index():
    """Return homepage."""

    user_info = None

    return render_template("homepage.html", user_info = user_info)





####### Log In #######
@app.route("/login", methods = ["GET", "POST"])
def login():
    """Return login page."""

    if request.method == "POST":
        email = request.form.get("email") #Get email from login form
        password = request.form.get("password") #Get password from login form
        user = crud.all_user_info_by_email(email) #Get all of user's data (from searching by entered email)

        if user is None: #If the user is not in the database, ERROR
            flash("Incorrect credentials.", category='danger')
            return redirect("/login")
        if user.password != password: #If the user's password is not equal to the saved password, ERROR
            flash("Incorrect credentials.", category='danger')
            return redirect("/login")
        if user:
            session["user_id"] = user.user_id #Create session cookie for user's id
            session["email"] = user.email #Create session cookie for user's email
            return redirect("/profile")

    #Load the page
    else:

        user_info = None

        return render_template("login.html", user_info = user_info)





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
        flash("Successful. Please log in.", category='success')
        return redirect("/login")

    else:
        user_info = None

        return render_template("signup.html", user_info = user_info)




####### Profile #######
@app.route("/profile", methods = ["GET", "POST"])
def profile():
    """Return profile page."""

    if "user_id" in session: #If user logged in and cookies are saved, get all their data
        email = session["email"]
        user_info = crud.all_user_info_by_email(email)
        user_id = user_info.user_id

    else: #If user not logged in, kick back to homepage
        flash("Must log in to view profile information.", category='danger')
        return redirect("/")

    reservations = []
    all_reservations = crud.all_reservations_by_user(user_id)
    for reservation in all_reservations:
        tasting_details_dict = {}
        tasting_details = crud.tasting_details_by_reservation(reservation.reservation_id)
        tasting_details_dict["tasting_name"] = tasting_details[0].tasting_name
        tasting_details_dict["tasting_photo"] = tasting_details[0].tasting_photo
        tasting_details_dict["tasting_date"] = reservation.reservation_date
        tasting_details_dict["tasting_time_end"] = reservation.reservation_date + timedelta(minutes=30)
        reservations.append(tasting_details_dict)

    return render_template("profile.html", user_info = user_info, reservations = reservations)




####### Search #######
@app.route("/search", methods = ["GET", "POST"])
def search():
    """Return search page where user can search for reservations and book them."""

    if "user_id" in session: #If user logged in and cookies are saved, get all their data
        email = session["email"]
        user_info = crud.all_user_info_by_email(email)

    else: #If user not logged in, kick back to homepage
        flash("Must log in to view profile information.", category='danger')
        return redirect("/")

    return render_template("search.html", user_info = user_info)





@app.route("/api/search", methods=["POST"])
def search_API():
    """Returns all tasting matches to front-end."""

    date = request.json['date']

    tasting_matches = []
    tasting_matches.clear()

    tastings = crud.all_tastings()
    reservations = crud.all_reservations()

    for tasting in tastings:
        tasting_matches_dict = {}
        tasting_matches_dict.clear()
        for reservation in reservations:
            if reservations is []:
                break
            if tasting.tasting_id == reservation.tasting_id:
                if reservation.reservation_date != date:
                    tasting_matches_dict["tasting_id"] = tasting.tasting_id
                    tasting_matches_dict["tasting_name"] = tasting.tasting_name
                    tasting_matches_dict["tasting_photo"] = tasting.tasting_photo
                    tasting_matches.append(tasting_matches_dict)
                else:
                    flash("No availbility with this date.", category='danger')

        tasting_matches_dict["tasting_id"] = tasting.tasting_id
        tasting_matches_dict["tasting_name"] = tasting.tasting_name
        tasting_matches_dict["tasting_photo"] = tasting.tasting_photo
        tasting_matches.append(tasting_matches_dict)

    #no duplicates in my results
    results = []
    for i in range(len(tasting_matches)):
        if tasting_matches[i] not in tasting_matches[i + 1:]:
            results.append(tasting_matches[i])

    return jsonify({'matches': results})





####### Reservations #######
@app.route("/reservations/<tasting_id>", methods = ["GET", "POST"])
def reservation(tasting_id):
    """Return reservation page."""

    if "user_id" in session: #If user logged in and cookies are saved, get all their data
        email = session["email"]
        user_info = crud.all_user_info_by_email(email)
        user_id = user_info.user_id

    if request.method == "POST":
        date = request.form.get("date")
        time = request.form.get("time")
        reservation_date = date + " " + time
        print(reservation_date)
        reservation = crud.create_reservation(user_id, reservation_date, tasting_id)
        db.session.add(reservation)
        db.session.commit()
        flash("Successfully reserved.", category='success')
        return redirect("/profile")

    return render_template("reservations.html", user_info = user_info, tasting_id = tasting_id)





if __name__ == "__main__":

    connect_to_db(app)

    app.run(
        host="0.0.0.0",
        use_reloader=False,
        use_debugger=False,
        passthrough_errors=True,
    )