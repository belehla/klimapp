# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 16:17:13 2022

@author: Hammerle
"""
import datetime as dt
import json
import random
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, flash


FOLDER = "src/"  # docker
# FOLDER = ""  # local

GOALS = {"money": {"title": "Money", "target": 1095, "legend": "Saved Money"},
         "miles": {"title": "Miles", "target": 15683, "legend": "Traveled Miles"},
         "cities": {"title": "Cities", "target": 100, "legend": "Visited Cities"},
         "trips": {"title": "Trips", "target": 300, "legend": "Number of Trips"}}

app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True
with open(f"{FOLDER}secret_key", "rb") as secretKeyFile:
    app.secret_key = secretKeyFile.read()


@app.route("/", methods=["GET"])
def index():
    trips = get_trips()
    progress = get_goal_progress(trips)
    last_trips = sorted(trips, key=lambda x:x["datetime"])[-3:]
    return render_template("index.html", progress=progress, trips=last_trips)


@app.route("/add-trip", methods=["GET", "POST"])
def add_trip():
    dt_now = dt.datetime.now().strftime("%Y-%m-%dT%H:%M")

    if request.method == "POST":
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


@app.route("/goal-details/<goal_id>", methods=["GET"])
def goal_details(goal_id):
    goal = GOALS[goal_id]
    trips = pd.DataFrame(get_trips()).sort_values("datetime")
    trips["month"] = pd.to_datetime(trips['datetime']).dt.to_period("M")
    trips["price"] = trips["price"].replace("", 0).astype(int)
    trips["cities"] = np.random.randint(0, 3, size=trips.shape[0])  # TODO: count cities

    trips["miles_cs"] = trips["miles"].cumsum()
    trips["money_cs"] = trips["price"].cumsum()
    trips["trips_cs"] = np.arange(trips.shape[0]) + 1
    trips["cities_cs"] = trips["cities"].cumsum()

    return render_template('goal_details.html', goal=goal, legend=goal["legend"],
                           values=trips[goal_id + "_cs"], labels=trips["datetime"])


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
    with open(f"{FOLDER}database.json") as file:
        trips = json.load(file)
    return trips


def add_trip_to_db(trip):
    trips = get_trips()
    trips.append(trip)
    with open(f"{FOLDER}database.json", "w") as file:
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
    # app.run()  # localhost
    app.run(host="0.0.0.0")  # in network
