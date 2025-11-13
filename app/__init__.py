from flask import Flask
from config import Config

import logging
from logging.handlers import *
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Sets up logging but only if no handlers exist yet and avoids duplicate logs when the debug reloader runs
    if not app.logger.handlers:
        logDir = "logs"
        # Ensures that the logs directory exists
        os.makedirs(logDir, exist_ok = True)
        logFile = os.path.join(logDir, "registration.log")

        # Logs to a file that rotates when it gets too big
        fileHandler = RotatingFileHandler(
            logFile, maxBytes=10240, backupCount=5)

        # decides the format of the log which is: timestamp, level, and message.
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")

        fileHandler.setFormatter(formatter)

        # Logs INFO and above to this file.
        fileHandler.setLevel(logging.INFO)

        # attaches this handler to the apps logger.
        app.logger.addHandler(fileHandler)
        app.logger.setLevel(logging.INFO)

    from .routes import main
    app.register_blueprint(main)

    return app