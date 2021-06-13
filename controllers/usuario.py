from flask_restful import Resource, reqparse, request
from models.usuario import UsuarioModel
from re import search, fullmatch
from sqlalchemy.exc import IntegrityError
from cryptography.fernet import Fernet
from os import environ
from dotenv import load_dotenv
import json
from db.db import db
from datetime import datetime, timedelta
from utils.mailer import enviarCorreo
import bcrypt
load_dotenv()

PATRON_CORREO = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
PATRON_PASSWORD = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#&?])[A-Za-z\d@$!%*#&?]{6,}$'


class RegistroController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'nombre',
        type=str,
        required=True,
        location='json',
        help='Falta el nombre'
    )
    serializer.add_argument(
        'apellido',
        type=str,
        required=True,
        location='json',
        help='Falta el apellido'
    )
    serializer.add_argument(
        'correo',
        type=str,
        required=True,
        location='json',
        help='Falta el correo'
    )
    serializer.add_argument(
        'password',
        type=str,
        required=True,
        location='json',
        help='Falta el password'
    )

    def post(self):
        data = self.serializer.parse_args()
        correo = data.get('correo')
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        password = data.get('password')

        if search(PATRON_CORREO, correo) and fullmatch(PATRON_PASSWORD, password):
            try:
                nuevoUsuario = UsuarioModel(nombre, apellido, correo, password)
                nuevoUsuario.save()
                return {
                    "success": True,
                    "content": nuevoUsuario.json(),
                    "message": "Usuario registrado exitosamente"
                }, 201
            except IntegrityError as error:
                print(error)
                return {
                    "success": False,
                    "content": None,
                    "message": "Correo ya existe"
                }, 400
            except:
                return{
                    "success": False,
                    "content": None,
                    "message": "Error inesperado!"
                }, 400
        else:
            return {
                "success": False,
                "content": None,
                "message": "Correo o password incorrecto"
            }, 400


class ForgotPasswordController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        "correo",
        type=str,
        required=True,
        location='json',
        help='Falta el correo'
    )

    def post(self):
        data = self.serializer.parse_args()
        correo = data['correo']

        if search(PATRON_CORREO, correo):
            usuario = db.session.query(
                UsuarioModel).filter_by(usuarioCorreo=correo).first()
            if not usuario:
                return {
                    "success": False,
                    "content": None,
                    "message": "Usuario no registrado"
                }, 400
            fernet = Fernet(environ.get("FERNET_SECRET"))
            payload = {
                "fecha_caducidad": str(datetime.now()+timedelta(minutes=30)),
                "correo": correo
            }
            payload_json = json.dumps(payload)
            token = fernet.encrypt(bytes(payload_json, 'utf-8'))
            link = request.host_url+'recuperarPassword/'+token.decode('utf-8')
            respuesta = enviarCorreo(
                usuario.usuarioCorreo, usuario.usuarioNombre, link)
            if respuesta:
                return {
                    "success": True,
                    "content": None,
                    "message": "Correo enviado exitosamente"
                }
            else:
                return {
                    "success": False,
                    "content": None,
                    "message": "Error al enviar el correo, intente nuevamente"
                }, 500
        else:
            return {
                "success": False,
                "content": None,
                "message": "Formato de correo incorrecto"
            }, 400


class ResetPasswordController(Resource):
    serializer = reqparse.RequestParser(bundle_errors=True)
    serializer.add_argument(
        'correo',
        type=str,
        required=True,
        help='Falta el correo',
        location='json'
    )
    serializer.add_argument(
        'new_password',
        type=str,
        required=True,
        help='Falta el new_password',
        location='json'
    )

    def post(self):
        data = self.serializer.parse_args()
        if search(PATRON_CORREO, data['correo']):
            usuario = db.session.query(UsuarioModel).filter_by(
                usuarioCorreo=data['correo']).first()
            if usuario:
                if fullmatch(PATRON_PASSWORD, data['new_password']):
                    print(usuario.usuarioPassword)
                    passwordBytes = bytes(data['new_password'], "utf-8")
                    passwordHash = bcrypt.hashpw(
                        passwordBytes, bcrypt.gensalt())
                    passwordString = passwordHash.decode("utf-8")
                    usuario.usuarioPassword = passwordString
                    usuario.save()
                    print(usuario.usuarioPassword)
                    return {
                        "success": True,
                        "content": usuario.json(),
                        "message": "La contraseña se actualizo exitosamente"
                    }
                else:
                    return {
                        "success": False,
                        "content": None,
                        "message": "La contraseña debe de tener al menos 6 caracteres , una mayus, una minus, un numero y un caracter especial"
                    }
            else:
                return {
                    "success": False,
                    "content": None,
                    "message": "Usuario no encontrado"
                }, 400
        else:
            return {
                "success": False,
                "content": None,
                "message": "Formato de correo incorrecto"
            }, 400
