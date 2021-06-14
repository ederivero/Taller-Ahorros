from flask import Flask, request, render_template
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
from db.db import db
from os import path, environ
from datetime import timedelta
from controllers.usuario import (
    RegistroController, ResetPasswordController, ForgotPasswordController)
from controllers.movimiento import MovimientosController
from utils.jwt_config import autenticador, identificador, manejo_error_JWT
import pathlib
import sqlite3
import platform

load_dotenv()


SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Ahorros Flask - Swagger Documentation"
    }
)
app = Flask(__name__)
CORS(app)

app.register_blueprint(swagger_blueprint)
if environ.get('PRODUCTION'):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI')
else:
    DB_ROUTE = path.join(
        pathlib.Path(__file__).parent.absolute(), 'db', 'test.db')
    sqlite3.connect(DB_ROUTE).close()
    if platform.system() == 'Windows':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(DB_ROUTE)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}'.format(
            DB_ROUTE)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get("JWT_SECRET")
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
api = Api(app)
jwt = JWT(app, autenticador, identificador)
jwt.jwt_error_callback = manejo_error_JWT

db.init_app(app)

db.create_all(app=app)

api.add_resource(RegistroController, '/register')
api.add_resource(ResetPasswordController, '/reset-password')
api.add_resource(ForgotPasswordController, '/forgot-password')
api.add_resource(MovimientosController, '/transactions')


@app.route('/', methods=['GET'])
def inicio():
    return render_template('index.jinja')


if __name__ == '__main__':
    app.run(debug=True)
