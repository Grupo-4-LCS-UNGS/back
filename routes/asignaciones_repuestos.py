from flask import Blueprint, request

from models.asignacion_repuestos import AsignacionRepuestos

asignaciones_repuestos = Blueprint('asignaciones_repuestos', __name__)

@asignaciones_repuestos.route('/asignaciones_repuestos/')
def listar_asignaciones():
    return AsignacionRepuestos.listar_json()

@asignaciones_repuestos.route('/asignaciones_repuestos/por_mantenimiento/<int:id>', methods=['GET'])
def listar_asignaciones_por_mantenimiento(id):
    return AsignacionRepuestos.listar_por_mantenimiento(id)


@asignaciones_repuestos.route('/asignaciones_repuestos/', methods=['POST'])
def alta_asignacion():
    data = request.get_json()
    data.pop('fecha', None)
    AsignacionRepuestos.agregar(AsignacionRepuestos(**data))
    return 'OK', 202

@asignaciones_repuestos.route('/asignaciones_repuestos/<int:id>', methods=['DELETE'])
def baja_asignacion(id):
    asignacion = AsignacionRepuestos.encontrarPorId(id)
    if asignacion == None:
        return 'Asignación de repuestos no encontrada', 404
    AsignacionRepuestos.eliminar(asignacion)
    return 'OK', 202