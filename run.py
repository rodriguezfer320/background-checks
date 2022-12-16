from flask import Flask
from app.config import Config
from app.routes.api import api_scope

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(api_scope, url_prefix='/api/')

if __name__ == '__main__':
	app.run()