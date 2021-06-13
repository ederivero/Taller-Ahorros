from flask import Flask, request, render_template
from flask_restful import Api
from flask_jwt import JWT
from dotenv import load_dotenv
from db.db import db
from os import path, environ
from datetime import timedelta
from controllers.usuario import (
    RegistroController, ResetPasswordController, ForgotPasswordController)
from controllers.movimiento import MovimientosController
from utils.jwt_config import autenticador, identificador
import pathlib

load_dotenv()


DB_ROUTE = environ.get('DATABASE_URI') if environ.get('PRODUCCION') else path.join(
    pathlib.Path(__file__).parent.absolute(), 'db', 'test.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{}'.format(DB_ROUTE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get("JWT_SECRET")
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
api = Api(app)
jwt = JWT(app, autenticador, identificador)

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
