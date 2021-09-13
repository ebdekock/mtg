#!/bin/bash

# Init db on startup
# Ephemereal user DB on container, will change once we have proper auth
flask init-db

# Start Flask
flask run --host="$FLASK_HOST" --port="$FLASK_PORT"
