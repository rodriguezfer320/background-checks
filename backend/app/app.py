from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from .config import config
from .database import db
from .routes import api

class Application:

    def __init__(self):
        # app
        self.app = Flask(__name__, static_folder="/app/static")

        # configuración
        self.app.config.from_object(config['development'])

        # extensiones
        CORS(self.app, resources=r'/api/*', origins=['http://localhost:3000', 'http://192.168.0.23:3000'], methods=['GET', 'POST', 'PUT', 'DELETE'])
        Api(self.app)
        db.init_app(self.app)

        # rutas de la api
        self.app.register_blueprint(api)