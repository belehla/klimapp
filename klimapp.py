# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 16:17:13 2022

@author: Hammerle
"""
import datetime as dt
from flask import Flask, render_template, request, flash


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
with open("secret_key", "rb") as secretKeyFile:
    app.secret_key = secretKeyFile.read()


GOALS = {"money": {"title": "saved money", "target": 800},
         "miles": {"title": "miles", "target": 8000},
         "cities": {"title": "cities", "target": 80},
         "trips": {"title": "trips", "target": 80}}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")


@app.route("/add-trip", methods=["GET", "POST"])
def add_trip():
    dt_now = dt.datetime.now().strftime("%Y-%m-%dT%H:%M")

    if request.method == "GET":
        return render_template("add_trip.html", dt_now=dt_now)

    elif request.method == "POST":
        trip = {
            "type": request.form.get("type"),
            "start": request.form.get("start"),
            "destination": request.form.get("destination"),
            "comment": request.form.get("comment"),
            "datetime": request.form.get("datetime"),
            "price": request.form.get("price")
        }
        print(trip, flush=True)
        upload_check = trip["start"] and trip["destination"]
        if upload_check:
            flash("Trip was added!", "success")
        else:
            flash("Error in data, try again!", "danger")
        return render_template("add_trip.html", trip=trip, dt_now=dt_now)


@app.route("/goals", methods=["GET"])
def goals():
    return render_template("goals.html")


@app.route("/goal-details/<goal_id>", methods=["GET", "POST"])
def goal_details(goal_id):
    if request.method == "GET":
        return render_template("goal_details.html", goal=GOALS[goal_id])


@app.route("/rewards", methods=["GET"])
def rewards():
    return render_template("rewards.html")


@app.route("/ticket", methods=["GET"])
def ticket():
    return render_template("ticket.html")


@app.route("/history", methods=["GET"])
def history():
    return render_template("history.html")


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run()  # localhost
    # app.run(host="0.0.0.0")  # in network
