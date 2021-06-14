from models.usuario import UsuarioModel
from bcrypt import checkpw
from db.db import db


class Usuario:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __str__(self):
        return "Usuario con el id ='%s' y username='%s'" % (self.id, self.username)


def autenticador(username, password):
    """Funcion encargado en mi JWT de validar las credenciales si estas son ingresadas correctamente (si hacen match con algun usuario"""
    if username and password:
        usuario = db.session.query(
            UsuarioModel).filter_by(usuarioCorreo=username).first()
        if usuario:
            if checkpw(bytes(password, 'utf-8'), bytes(usuario.usuarioPassword, 'utf-8')):
                return Usuario(usuario.usuarioId, usuario.usuarioCorreo)
    return None


def identificador(payload):
    """Sirve para que una vez el usuario ya este logeado y tenga su JWT pueda realizar peticiones a una ruta protegica y esta funcion sera la encargada de identificar a dicho usuario y devolver su informacion"""
    if(payload['identity']):
        usuario = db.session.query(UsuarioModel).filter_by(
            usuarioId=payload['identity']).first()
        if usuario:
            return usuario
    return None


# funcion para personalizar el mensaje de error de mi libreria de JWT
def manejo_error_JWT(error):
    print(error)
    respuesta = {
        "success": False,
        "content": None,
        "message": None
    }
    if error.error == 'Authorization Required':
        respuesta["message"] = "Se necesita una token para esta peticion"
    elif error.error == 'Bad Request':
        respuesta["message"] = "Credenciales invalidas"
    elif error.description == "Signature has expired":
        respuesta["message"] = "Token ya expiro"
    elif error.description == "Signature verification failed":
        respuesta["message"] = "Token invalida"
    elif error.description == "Unsupported authorization type":
        respuesta["message"] = "Debe de mandar la token con el prefijo Bearer"
    else:
        respuesta["message"] = "Error desconocido"

    return respuesta, error.status_code
    # 401 => unauthorized => no autorizado
