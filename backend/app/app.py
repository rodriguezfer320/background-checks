from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from .config import config
from .database import db
from .routes import api
from decouple import config as configEnv

def create_app():
    # app
    app = Flask(__name__)

    # configuración
    app.config.from_object(config[configEnv('ENVIRONMENT')])

    # extensiones
    CORS(app, resources=r'/fs-uv/bc/api/*', origins=['*'], methods=['GET', 'POST', 'PUT'])
    Api(app)
    db.init_app(app)

    # se registran las rutas de la api
    app.register_blueprint(api)
    
    return app, configEnv('ENVIRONMENT') == 'production'