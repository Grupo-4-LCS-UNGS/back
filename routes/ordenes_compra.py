from flask import Blueprint, request

from models.orden_compra import OrdenCompra

ordenes_compras = Blueprint('ordenes_compras', __name__)

@ordenes_compras.route('/ordenes_compras/')
def listar_ordenes():
    return OrdenCompra.listar_json()

@ordenes_compras.route('/ordenes_compras/<int:id>', methods=['PUT'])
def actualizar_orden(id):
    orden_compra = OrdenCompra.encontrarPorId(id)
    if orden_compra == None:
        return 'Orden de compra no encontrada', 404
    data = request.get_json()
    orden_compra.estado = data.get('estado', orden_compra.estado)
    OrdenCompra.actualizar()
    return 'OK', 202

@ordenes_compras.route('/ordenes_compras/<int:id>', methods=['DELETE'])
def baja_orden(id):
    orden_compra = OrdenCompra.encontrarPorId(id)
    if orden_compra == None:
        return 'Orden de compra no encontrada', 404
    OrdenCompra.eliminar(orden_compra)
    return 'OK', 202