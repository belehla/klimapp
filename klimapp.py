# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 16:17:13 2022

@author: Hammerle
"""
import datetime as dt
import json
import random
from flask import Flask, render_template, request, flash


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
with open("secret_key", "rb") as secretKeyFile:
    app.secret_key = secretKeyFile.read()


GOALS = {"money": {"title": "saved money", "target": 1095},
         "miles": {"title": "miles", "target": 15683},
         "cities": {"title": "cities", "target": 100},
         "trips": {"title": "trips", "target": 300}}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        trips = get_trips()
        progress = get_goal_progress(trips)
        last_trips = sorted(trips, key=lambda x:x["datetime"])[-3:]
        return render_template("index.html", progress=progress, trips=last_trips)


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
            "price": request.form.get("price") or int(random.random() * 100),  # TODO: replace with api req if nan
            "miles": int(random.random() * 300)  # TODO: replace with api req
        }
        upload_check = trip["start"] and trip["destination"]
        add_trip_to_db(trip)

        if upload_check:
            flash(f"Trip {trip['start']} - {trip['destination']} was added "
                  f"with {trip['price']} € and {trip['miles']} miles!", "success")
        else:
            flash("Error in data, try again!", "danger")
        return render_template("add_trip.html", dt_now=dt_now)


@app.route("/goals", methods=["GET"])
def goals():
    trips = get_trips()
    progress = get_goal_progress(trips)
    return render_template("goals.html", progress=progress, goals=GOALS)


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


def get_trips():
    with open("database.json") as file:
        trips = json.load(file)
    return trips


def add_trip_to_db(trip):
    trips = get_trips()
    trips.append(trip)
    with open("database.json", "w") as file:
        json.dump(trips, file, indent=4)


def get_goal_progress(trips):
    progress = {
        "no_trips": len(trips),
        "sum_money": sum(int(tr["price"]) for tr in trips if tr["price"] != ""),
        "no_cities": len(set([tr["start"].lower() for tr in trips] +
                             [tr["destination"].lower() for tr in trips])),
        "sum_miles": sum([tr["miles"] for tr in trips])
    }
    return progress


if __name__ == "__main__":
    app.run()  # localhost
    # app.run(host="0.0.0.0")  # in network
