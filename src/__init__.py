from logging import FileHandler, WARNING, INFO, DEBUG
from logging.config import dictConfig
from datetime import datetime as dt
import logging

from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify, request
from marshmallow.exceptions import ValidationError
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask.logging import default_handler
from src.logs import logging_config



db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

# file_handler = FileHandler('src/logs/errors.log')
# file_handler.setLevel(WARNING)
#
# login_fh = FileHandler('src/logs/logins.log')
# login_fh.setLevel(INFO)
#
# requests_log = FileHandler('src/logs/requests.log')
# requests_log.setLevel(INFO)


def create_app():
	#dictConfig(logging_config)
	app = Flask(__name__)
	app.config.from_object("src.default_settings.app_config")

	db.init_app(app)
	ma.init_app(app)
	bcrypt.init_app(app)
	jwt.init_app(app)
	migrate.init_app(app, db)

	app.logger.removeHandler(default_handler)

	# login_logger = logging.getLogger('login_logger')
	# login_logger.addHandler(login_fh)
	#
	# req_logger = logging.getLogger('requests_log')
	# req_logger.addHandler('requests_log')

	from src.commands import db_commands
	app.register_blueprint(db_commands)

	from src.controllers import registerable_controllers

	for controller in registerable_controllers:
		app.register_blueprint(controller)

	@app.errorhandler(ValidationError)
	def handle_bad_request(error):
		return jsonify(error.messages), 400

	# @app.after_request
	# def after_request(response):
	# 	""" Logging after every request. """
	# 	logger = logging.getLogger("req_log")
	# 	logger.warning(
	# 		"%s [%s] %s %s %s %s %s %s %s",
	# 		request.remote_addr,
	# 		dt.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
	# 		request.method,
	# 		request.path,
	# 		request.scheme,
	# 		response.status,
	# 		response.content_length,
	# 		request.referrer,
	# 		request.user_agent,
	# 	)
	# 	return response

	return app
