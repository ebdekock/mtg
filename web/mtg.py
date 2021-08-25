from datetime import datetime, timedelta

import pymongo
from flask import Blueprint, current_app, render_template, request

from web.auth import login_required
from web.kafka import get_kafka_producer
from web.mongodb import get_mongo_db

mtg_bp = Blueprint("mtg", __name__)


@mtg_bp.route("/", methods=("GET", "POST"))
@login_required
def index():
    """Search page, sends search results to Kafka to be processed"""
    producer = get_kafka_producer()

    if request.method == "POST":
        search = request.form["card"]
        producer.send(f'{current_app.config["KAFKA_TOPIC"]}', value={"search": search})

    return render_template("mtg/index.html")


@mtg_bp.route("/results", methods=("GET",))
@login_required
def results():
    """Results page, show latest search and link to most recent"""
    mongo = get_mongo_db()
    db = mongo.get_collection()

    last_result = db.find_one({}, sort=[("datetime", pymongo.DESCENDING)])

    search_cursor = db.find(
        {
            "datetime": {
                "$gte": datetime.now() - timedelta(days=7),
                "$lt": datetime.now(),
            }
        }
    )
    results = []
    for result in search_cursor:
        results.append(result)
    results.reverse()

    return render_template("mtg/results.html", results=results, last_result=last_result)


@mtg_bp.route("/result/<search_id>", methods=("GET",))
@login_required
def result(search_id):
    """Single search result page, show its results"""
    mongo = get_mongo_db()
    db = mongo.get_collection()
    result = db.find_one({"_id": search_id})

    return render_template("mtg/result.html", result=result)
