from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from db.db import db
from models.usuario import UsuarioModel
from models.movimiento import MovimientoModel


class MovimientosController(Resource):
    movimientoSerializer = reqparse.RequestParser(bundle_errors=True)

    movimientoSerializer.add_argument(
        'nombre',
        type=str,
        required=True,
        help='Falta el nombre',
        location='json',
    )
    movimientoSerializer.add_argument(
        'monto',
        type=float,
        required=True,
        help='Falta el monto',
        location='json',
    )
    movimientoSerializer.add_argument(
        'fecha',
        type=str,
        required=False,
        location='json',
    )
    movimientoSerializer.add_argument(
        'imagen',
        type=str,
        required=False,
        location='json',
    )
    movimientoSerializer.add_argument(
        'tipo',
        type=str,
        required=True,
        help='Falta el tipo',
        location='json',
        choices=['ingreso', 'egreso']
    )

    @jwt_required()
    def post(self):
        data = self.movimientoSerializer.parse_args()
        usuario: UsuarioModel = current_identity
        try:
            fecha = datetime.strptime(data['fecha'], '%Y-%m-%d')
            nuevoMovimiento = MovimientoModel(
                data['nombre'], data['monto'], fecha, data['tipo'], usuario.usuarioId)
            nuevoMovimiento.save()
            return {
                "success": True,
                "message": "Movimiento registrado exitosamente",
                "content": nuevoMovimiento.json(),
            }
        except Exception as error:
            print(error)
            return {
                "success": False,
                "message": "Formato de fecha incorrecto, el formato es YYYY-MM-DD",
                "content": None
            }

    @jwt_required()
    def get(self):
        usuario: UsuarioModel = current_identity
        transactions = db.session.query(MovimientoModel).filter_by(
            usuario=usuario.usuarioId).order_by(MovimientoModel.movimientoFecha.desc()).all()
        data = []
        for transaction in transactions:
            data.append(transaction.json())
        return {
            "success": True,
            "content": data,
            "message": None
        }


class BalanceController(Resource):
    @jwt_required()
    def post(self):
        serializer = reqparse.RequestParser(bundle_errors=True)
        serializer.add_argument(
            'fecha_inicio',
            type=str,
            required=True,
            help='Falta la fecha_inicio',
            location='json'
        )
        serializer.add_argument(
            'fecha_fin',
            type=str,
            required=True,
            help='Falta la fecha_fin',
            location='json'
        )
        data = serializer.parse_args()
        usuario: UsuarioModel = current_identity
        movimientos: list[MovimientoModel] = db.session.query(
            MovimientoModel).filter(MovimientoModel.usuario == usuario.usuarioId, MovimientoModel.movimientoFecha.between(
                data.get('fecha_inicio'), data.get('fecha_fin'))).all()
        ingresos = 0.0
        egresos = 0.0
        for movimiento in movimientos:
            if movimiento.movimientoTipo == "egreso":
                egresos += movimiento.movimientoMonto
            elif movimiento.movimientoTipo == "ingreso":
                ingresos += movimiento.movimientoMonto
        return {
            "success": True,
            "content": {
                "ingresos": ingresos,
                "egresos": egresos
            },
            "message": None
        }
