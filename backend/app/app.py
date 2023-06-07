from flask import Flask, json, jsonify
from flask_smorest import Api
from flask_cors import CORS
from .config import config
from .database import db
from .routes import api

def create_app():
    # app
    app = Flask(__name__)

    # configuración
    app.config.from_object(config['development'])

    # extensiones
    CORS(app, resources=r'/fs-uv/api/*', origins=['http://localhost:3000'], methods=['GET', 'POST', 'PUT', 'DELETE'])
    Api(app)
    db.init_app(app)

    # se registran las rutas de la api
    app.register_blueprint(api)
    
    return app