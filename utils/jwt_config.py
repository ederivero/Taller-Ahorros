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
    # primero valido si hay un username y un password
    if username and password:
        # busco ese usuario en la bd segun su correo como username
        usuario = db.session.query(
            UsuarioModel).filter_by(usuarioCorreo=username).first()
        # si hay el usuario
        if usuario:
            # valido su password
            # la funcion checkpw toma dos parametros, el primero es la contraseña actual y el segundo es la contraseña almacenada en la bd, internamente las validara y si son, retornara True, caso contrario retornara False

            if checkpw(bytes(password, 'utf-8'), bytes(usuario.usuarioPassword, 'utf-8')):
                print("Es el usuario")
                # si la contraseña es correcta
                # esto me servira para agregarlo en el payload (la parte intermedia de la jwt)
                return Usuario(usuario.usuarioId, usuario.usuarioCorreo)
            else:
                print("La contraseña no coincide")
                return None
        else:
            print("El usuario no existe")
            return None
    else:
        print("Falta el usuario o la password")
        return None


def identificador(payload):
    """Sirve para que una vez el usuario ya este logeado y tenga su JWT pueda realizar peticiones a una ruta protegica y esta funcion sera la encargada de identificar a dicho usuario y devolver su informacion"""
    # el payload retornara un diccionario
    print(payload)
    if(payload['identity']):
        # identity se almacenara el id del usuario
        usuario = db.session.query(UsuarioModel).filter_by(
            usuarioId=payload['identity']).first()
        if usuario:
            return usuario
        else:
            # el usuario en la token no existe en mi bd ( IMPOSIBLE!! )
            return None
    else:
        # en mi payload no hay la llave identity
        return None


# funcion para personalizar el mensaje de error de mi libreria de JWT
def manejo_error_JWT(error):
    respuesta = {
        "success": False,
        "content": None,
        "message": None
    }
    print(error)
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
