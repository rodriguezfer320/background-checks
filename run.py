from flask import Flask
from config import config
from app.routes import background_check

# create the app
app = Flask(__name__)


if __name__ == '__main__':
	# configuration
	app.config.from_object(config['development'])

	# blueprints
	app.register_blueprint(background_check.background_check_scope, url_prefix='/api/')

	# initialize the app
	app.run()