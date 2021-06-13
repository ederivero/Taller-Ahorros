from db.db import db
from sqlalchemy import Column, types, orm
import bcrypt


class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    usuarioId = Column(name='id', type_=types.Integer, primary_key=True,
                       unique=True, autoincrement=True, nullable=False)
    usuarioNombre = Column(
        name='nombre', type_=types.String(45), nullable=False)
    usuarioApellido = Column(
        name='apellido', type_=types.String(45), nullable=False)
    usuarioCorreo = Column(
        name='correo', type_=types.String(25), nullable=False, unique=True)
    usuarioPassword = Column(name='password', type_=types.TEXT, nullable=False)

    movimientos = orm.relationship(
        'MovimientoModel', backref='movimientoUsuario')

    def __init__(self, nombre, apellido, correo, password):
        self.usuarioNombre = nombre
        self.usuarioApellido = apellido
        self.usuarioCorreo = correo
        self.usuarioPassword = bcrypt.hashpw(
            bytes(password, "utf-8"), bcrypt.gensalt()).decode('utf-8')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "usuarioId": self.usuarioId,
            "usuarioNombre": self.usuarioNombre,
            "usuarioApellido": self.usuarioApellido,
            "usuarioCorreo": self.usuarioCorreo,
        }
