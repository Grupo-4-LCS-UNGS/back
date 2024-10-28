from flask import Blueprint, request

from models.proveedor import Proveedor

proveedores = Blueprint('proveedores', __name__)

@proveedores.route('/proveedores/')
def listar_proveedores():
    return Proveedor.listar_json()

@proveedores.route('/proveedores/', methods=['POST'])
def alta_proveedor():
    data = request.get_json()
    Proveedor.agregar(Proveedor(**data))
    return Proveedor.listar_json()

@proveedores.route('/proveedores/<int:id>', methods=['PUT'])
def actualizar_proveedor(id):
    proveedor = Proveedor.encontrarPorId(id)
    if proveedor == None:
        return 'Proveedor no encontrado', 404
    data = request.get_json()
    proveedor.nombre = data.get('nombre', proveedor.nombre)
    proveedor.direccion = data.get('direccion', proveedor.direccion)
    proveedor.telefono = data.get('telefono', proveedor.telefono)
    proveedor.cuit = data.get('cuit', proveedor.cuit)
    Proveedor.actualizar()
    return Proveedor.listar_json()

@proveedores.route('/proveedores/<int:id>', methods=['DELETE'])
def baja_proveedor(id):
    proveedor = Proveedor.encontrarPorId(id)
    if proveedor == None:
        return 'Proveedor no encontrado', 404
    Proveedor.eliminar(proveedor)
    return Proveedor.listar_json()
