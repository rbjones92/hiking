import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, lookup
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hikes.db")

os.environ["API_KEY"]="a04c130fab02d624acda50390b5407ce"

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# i deleted the route for deleting/deregister because wtf

@app.route("/log")
def log():
    """Show record of hikes"""
    hikes = db.execute("SELECT * FROM hikes")
    return render_template("log.html", hikes=hikes)

@app.route("/halfdome")
def halfdome():
    """Show history of half dome"""
    return render_template("halfdome.html")

@app.route("/weather")
def weather():
    """Show history of weather"""
    return render_template("weather.html")

@app.route("/calendar")
def calendar():
    """Show calendar page"""
    return render_template("calendar.html")

@app.route("/refresh")
def calendar_refresh():
    import gcal_conn
    gcal_conn.delete_events(gcal_conn.connect())
    gcal_conn.create_events(gcal_conn.connect())
    """Show calendar page"""
    return render_template("calendar.html")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # TODO: Add the user's entry into the database
        location = request.form.get("location")
        date = request.form.get("date")
        distance = request.form.get("distance")
        db.execute("INSERT INTO hikes (location, date, distance) VALUES (?, ?, ?)", location, date, distance)
        return redirect("/")

    else:
        # TODO: Display the entries in the database on log.html
        hikes=db.execute("SELECT * FROM hikes")
        return render_template("log.html", hikes=hikes)

