import pathlib
import sqlite3
import platform
import json
from flask import Flask, render_template
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from os import path, environ
from db.db import db
from controllers.usuario import (
    RegistroController, ResetPasswordController, ForgotPasswordController)
from controllers.movimiento import BalanceController, MovimientosController
from utils.jwt_config import autenticador, identificador, manejo_error_JWT

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
api.add_resource(BalanceController, '/balance')


@app.route("/recuperarPassword/<string:token>")
def recuperar_password(token):

    fernet = Fernet(environ.get("FERNET_SECRET"))
    # decrypt(b'token')
    # el metodo decrypt recibe una token pero en formato de bytes y luego si es que cumple con la contraseña devolvera el mensaje encriptado pero en bytes, y para convertirlo a string usarmos el metodo decode
    try:
        respuesta = fernet.decrypt(bytes(token, 'utf-8')).decode('utf-8')
        # el metodo loads convierte un json a un diccionario
        respuesta_diccionario = json.loads(respuesta)
        fecha_caducidad = datetime.strptime(
            respuesta_diccionario['fecha_caducidad'], '%Y-%m-%d %H:%M:%S.%f')
        # si la fecha de caducidad es mayor que la hora actual, aun se podra realizar el cambio de contraseña, caso contrario, indicar que la token ya vencio
        if fecha_caducidad > datetime.now():
            return render_template('recovery_password.jinja', correo=respuesta_diccionario['correo'])
        else:
            return render_template('bad_token.jinja')

    except Exception as error:
        print(error)
        return render_template('bad_token.jinja')


@app.route('/', methods=['GET'])
def inicio():
    return render_template('index.jinja')


if __name__ == '__main__':
    app.run(debug=True)
