from flask import request
from flask import Blueprint

from models.repuesto import Repuesto

repuestos = Blueprint('repuestos', __name__)

@repuestos.route('/repuestos/')
def listar_repuestos():
    return Repuesto.listar_json()

@repuestos.route('/repuestos/<int:id>')
def obtener_repuesto(id):
    repuesto = Repuesto.encontrarPorId(id)
    if repuesto == None:
        return 'Repuesto no encontrado', 404
    return repuesto.serialize()

@repuestos.route('/repuestos/', methods=['POST'])
def alta_repuesto():
    data = request.get_json()
    Repuesto.agregar(Repuesto(**data))
    return 'OK', 202

@repuestos.route('/repuestos/<int:id>', methods=['DELETE'])
def baja_repuesto(id):
    repuesto = Repuesto.encontrarPorId(id)
    if repuesto == None:
        return 'Repuesto no encontrado', 404
    Repuesto.eliminar(repuesto)
    return 'OK', 202