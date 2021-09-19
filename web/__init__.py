import os

from flask import Flask

from web.filters import humanize_ts
from web.mtg import mtg_bp


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "web.sqlite"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists, run time data lives here
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Add routes
    app.register_blueprint(mtg_bp)
    app.add_url_rule("/", endpoint="index")

    # Add jinja filters
    app.jinja_env.filters["humanize"] = humanize_ts

    return app
