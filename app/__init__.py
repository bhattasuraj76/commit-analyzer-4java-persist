import json
import logging
import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app():
    # create the flask app
    flask_app = Flask(__name__, instance_relative_config=False, template_folder='./views')

    # http://exploreflask.com/en/latest/configuration.html#configuring-based-on-environment-variables
    def configure_app():
        # Load the default configuration
        flask_app.config.from_object("app.config.default")

        # Load the file specified by the APP_CONFIG_FILE env variable
        # variables defined here will override those in the default configuration
        if os.environ.get("APP_CONFIG_FILE") is not None:
            flask_app.config.from_envvar("APP_CONFIG_FILE")
            os.environ["ENVIRONMENT"] = flask_app.config["ENVIRONMENT"]
        else:
            flask_app.config.from_object("app.config.development")

        # Check for crucial env vars
        if not flask_app.config["SECRET_KEY"] and not os.environ.get("SECRET_KEY"):
            raise Exception("CRITICAL: No app secret detected")
        if not flask_app.config["SQLALCHEMY_DATABASE_URI"] and not os.environ.get(
            "SQLALCHEMY_DATABASE_URI"
        ):
            raise Exception("CRITICAL: No sqlalchemy URI detected.")

    configure_app()
    return flask_app


app = create_app()

# Create the sqlalchemy extension
db = SQLAlchemy()
# initialize the app with the extension
db.init_app(app)


def configure_logging(
):
    logging.basicConfig(filename=app.config["LOG_FILE"],
                        level=app.config["LOG_LEVEL"],
                        format='%(asctime)s %(levelname)s %(name)s %(threadName)s: %(message)s')
    logger = logging.getLogger(__name__)

    # add console logging to all logger for debugging
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)


def register_blueprints():
    with app.app_context():
        # Include routes
        from .routes.web import bp as webbp

        # Register blueprints
        app.register_blueprint(webbp)


def configure_template_filter():
    with app.app_context():
        @app.template_filter()
        def pretty_json(value):
            return json.dumps(value, sort_keys=True, indent=4, separators=(",", ": "))


configure_logging()
register_blueprints()
configure_template_filter()
