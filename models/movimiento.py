from sqlalchemy.sql.schema import ForeignKey
from db.db import db
from sqlalchemy import Column, types


class MovimientoModel(db.Model):
    __tablename__ = "movimientos"

    movimientoId = Column(name='id', type_=types.Integer, primary_key=True,
                          unique=True, autoincrement=True, nullable=False)
    movimientoNombre = Column(
        name='nombre', type_=types.String(45), nullable=False)
    movimientoMonto = Column(name='monto', type_=types.Float, nullable=False)
    movimientoFecha = Column(
        name='fecha', type_=types.Date, nullable=False)
    movimientoTipo = Column(
        name='tipo', type_=types.String(45), nullable=False)

    usuario = Column(ForeignKey(column='usuarios.id', ondelete="CASCADE"),
                     name='usuario_id', type_=types.Integer, nullable=False)

    def __init__(self, nombre, monto, fecha, tipo, usuario):
        self.movimientoNombre = nombre
        self.movimientoMonto = monto
        self.movimientoFecha = fecha
        self.movimientoTipo = tipo
        self.usuario = usuario

    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            "movimientoId": self.movimientoId,
            "movimientoNombre": self.movimientoNombre,
            "movimientoMonto": self.movimientoMonto,
            "movimientoFecha": str(self.movimientoFecha),
            "moviemientoTipo": self.movimientoTipo,
        }
