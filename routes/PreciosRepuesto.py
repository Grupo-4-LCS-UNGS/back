from flask import Blueprint, request
from models.proveedor import Proveedor
from models.PreciosRepuesto import PreciosRepuesto
from models.repuesto import Repuesto

precios_repuesto_bp = Blueprint('PreciosRepuesto', __name__)


@precios_repuesto_bp.route('/precios/')
def listar():
    return PreciosRepuesto.listar_json()

@precios_repuesto_bp.route('/precios/', methods=['POST'])
def alta():
    data = request.get_json()
    proveedor = Proveedor.encontrarPorId(data.get('id_proveedor'))
    repuesto = Repuesto.encontrarPorId(data.get('id_repuesto'))

    if proveedor is None or repuesto is None:
        return 'Error', 404

    PreciosRepuesto.agregar(PreciosRepuesto(**data))
    return 'OK', 202

@precios_repuesto_bp.route('/precios/<int:id_proveedor>/<int:id_repuesto>/', methods=['DELETE'])
def baja(id_proveedor, id_repuesto):
    proveedor_repuesto = PreciosRepuesto.encontrarPorId(id_proveedor, id_repuesto)
    if proveedor_repuesto is None:
        return 'No encontrado', 404
    PreciosRepuesto.eliminar(proveedor_repuesto)
    return  'OK', 202

@precios_repuesto_bp.route('/precios/<int:id_proveedor>/<int:id_repuesto>/', methods=['PUT'])
def actualizar(id_proveedor, id_repuesto):
    proveedor_repuesto = PreciosRepuesto.encontrarPorId(id_proveedor, id_repuesto)
    if proveedor_repuesto is None:
        return 'No encontrado', 404

    data = request.get_json()
    proveedor = Proveedor.encontrarPorId(id_proveedor)
    repuesto = Repuesto.encontrarPorId(id_repuesto)

    if proveedor is None or repuesto is None:
        return 'Error', 404

    proveedor_repuesto.costo = data.get('costo', proveedor_repuesto.costo)
    PreciosRepuesto.actualizar()
    return 'OK', 202


@precios_repuesto_bp.route('/precios/repuestos/<int:id_repuesto>/')
def obtener_por_repuesto(id_repuesto):
    precios = PreciosRepuesto.query.filter_by(id_repuesto=id_repuesto).all()
    return [precio.serialize() for precio in precios]
