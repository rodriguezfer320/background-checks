from flask import Flask
from flask_smorest import Api
from config import config
from app.routes import background_check, verification_request

# create the app
app = Flask(__name__, static_folder="static")

if __name__ == '__main__':
	# configuration
	app.config.from_object(config['development'])
	app.config["API_TITLE"] = "My API"
	app.config["API_VERSION"] = "v1"
	app.config["OPENAPI_VERSION"] = "3.0.2"

	#
	api = Api(app)

	# blueprints
	api.register_blueprint(background_check.bbc)
	api.register_blueprint(verification_request.bvr)

	# initialize the app
	app.run()