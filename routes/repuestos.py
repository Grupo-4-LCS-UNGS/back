from flask import request
from flask import Blueprint

from models.repuesto import Repuesto

repuestos = Blueprint('repuestos', __name__)

@repuestos.route('/repuestos/')
def listar_repuestos():
    return Repuesto.listar_json()

@repuestos.route('/api/repuestos/', methods=['POST'])
def alta_repuesto():
    data = request.get_json()
    Repuesto.agregar(Repuesto(**data))
    return Repuesto.listar_json()

@repuestos.route('/api/repuestos/<int:id>', methods=['DELETE'])
def baja_repuesto(id):
    repuesto = Repuesto.encontrarPorId(id)
    if repuesto == None:
        return 'Repuesto no encontrado', 404
    Repuesto.eliminar(repuesto)
    return Repuesto.listar_json()