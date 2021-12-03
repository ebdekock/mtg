import os
from collections import defaultdict
from datetime import datetime, timedelta

import pymongo
from flask import Blueprint, render_template, request, redirect, url_for

from web.kafka_lib import get_kafka_producer, get_current_queue_length
from web.utils import get_scrapyd_jobs_length
from web.mongodb import get_mongo_db

mtg_bp = Blueprint("mtg", __name__)


@mtg_bp.route("/search", methods=("GET", "POST"))
def search():
    """Search page, sends search results to Kafka to be processed"""
    topic = os.getenv("KAFKA_TOPIC")
    producer = get_kafka_producer()

    if request.method == "POST":
        search_terms = []
        search = request.form.get("card")
        if search:
            search_terms.append(search)

        searches = request.form.get("cards")
        if searches:
            for term in searches.split("\r\n"):
                # Janky cleanup of input
                # Remove second half of cards with //
                term = term.split("//")[0].strip().rstrip(",").strip()
                # Remove any brackets
                term = term.split("(")[0].strip().rstrip(",").strip()
                # Don't search blank lines
                if term:
                    search_terms.append(term)

        for search_term in search_terms:
            producer.send(f"{topic}", value={"search": search_term})

    return render_template("mtg/search.html")


@mtg_bp.route("/", methods=("GET",))
def index():
    """Redirect to latest results page"""
    mongo = get_mongo_db()
    db = mongo.get_collection()

    last_result = db.find_one({}, sort=[("datetime", pymongo.DESCENDING)])

    return redirect(
        url_for("mtg.result", search_id=last_result.get("_id")),
    )


@mtg_bp.route("/result/<search_id>", methods=("GET",))
def result(search_id):
    """Single search result page, show its results"""
    mongo = get_mongo_db()
    db = mongo.get_collection()

    current_search = db.find_one({"_id": search_id})
    recent_searches = db.find(
        {
            "datetime": {
                "$gte": datetime.now() - timedelta(days=7),
                "$lt": datetime.now(),
            }
        },
        sort=[("datetime", pymongo.DESCENDING)],
    )

    # Recent results
    results = defaultdict(list)
    for result in recent_searches:
        results[result.get("datetime").strftime("%d %b")].append(result)

    return render_template(
        "mtg/result.html",
        results=results,
        result=current_search,
        queue_length=get_current_queue_length(),
        running_jobs_length=get_scrapyd_jobs_length(),
    )
