from flask import Blueprint

from models.bitacora_asig_clientes import BitacoraAsigClientes

bitacora_clientes = Blueprint('bitacora_clientes', __name__)

@bitacora_clientes.route('/bitacora/clientes/')
def listar_bitacora():
    return BitacoraAsigClientes.listar_json()

@bitacora_clientes.route('/bitacora/clientes/<int:id>', methods=['DELETE'])
def baja_bitacora(id):
    asignacion = BitacoraAsigClientes.encontrarPorId(id)
    if asignacion is None:
        return 'Asignación no encontrada', 404
    BitacoraAsigClientes.eliminar(asignacion)
    return 'OK', 202