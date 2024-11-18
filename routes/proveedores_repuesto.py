from flask import Blueprint, request
from models.proveedor import Proveedor
from models.proveedor_repuesto import ProveedorRepuesto
from models.repuesto import Repuesto

proveedores_repuesto = Blueprint('proveedores_repuesto', __name__)
@proveedores_repuesto.route('/proveedores_repuesto/')
def listar():
    return ProveedorRepuesto.listar_json()

@proveedores_repuesto.route('/proveedores_repuesto/', methods=['POST'])
def alta():
    data = request.get_json()
    proveedor = Proveedor.encontrarPorId(data.get('id_proveedor'))
    repuesto = Repuesto.encontrarPorId(data.get('id_repuesto'))

    if proveedor is None or repuesto is None:
        return 'Error', 404

    ProveedorRepuesto.agregar(ProveedorRepuesto(**data))
    return 'OK', 202

@proveedores_repuesto.route('/proveedores_repuesto/<int:id_proveedor>/<int:id_repuesto>/', methods=['DELETE'])
def baja(id_proveedor, id_repuesto):
    proveedor_repuesto = ProveedorRepuesto.encontrarPorId(id_proveedor, id_repuesto)
    if proveedor_repuesto is None:
        return 'No encontrado', 404
    ProveedorRepuesto.eliminar(proveedor_repuesto)
    return  'OK', 202

@proveedores_repuesto.route('/proveedores_repuesto/<int:id_proveedor>/<int:id_repuesto>/', methods=['PUT'])
def actualizar(id_proveedor, id_repuesto):
    proveedor_repuesto = ProveedorRepuesto.encontrarPorId(id_proveedor, id_repuesto)
    if proveedor_repuesto is None:
        return 'No encontrado', 404

    data = request.get_json()
    proveedor = Proveedor.encontrarPorId(id_proveedor)
    repuesto = Repuesto.encontrarPorId(id_repuesto)

    if proveedor is None or repuesto is None:
        return 'Error', 404

    proveedor_repuesto.costo = data.get('costo', proveedor_repuesto.costo)
    ProveedorRepuesto.actualizar()
    return 'OK', 202