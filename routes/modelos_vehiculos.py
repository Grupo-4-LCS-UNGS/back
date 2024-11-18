from flask import Blueprint, request, jsonify

from models.modelo_vehiculo import ModeloVehiculo

modelos_vehiculos = Blueprint('modelos_vehiculos', __name__)

@modelos_vehiculos.route('/modelos_vehiculos/')
def listar_modelos():
    return ModeloVehiculo.listar_json()

@modelos_vehiculos.route('/modelos_vehiculos/', methods=['POST'])
def alta_modelo():
    data = request.get_json()
    ModeloVehiculo.agregar(ModeloVehiculo(**data))
    return ModeloVehiculo.listar_json()

@modelos_vehiculos.route('/modelos_vehiculos/<int:id>', methods=['PUT'])
def actualizar_marca(id):
    modelo = ModeloVehiculo.encontrarPorId(id)
    if modelo == None:
        return 'Modelo no encontrada', 404

    data = request.get_json()
    modelo.id_marca_vehiculo = data.get('id_marca_vehiculo')
    modelo.nombre = data.get('nombre', modelo.nombre)
    ModeloVehiculo.actualizar()
    return ModeloVehiculo.listar_json()

@modelos_vehiculos.route('/modelos_vehiculos/marca/<int:id_marca>', methods=['GET'])
def obtener_modelos_por_marca(id_marca):
    modelos = ModeloVehiculo.obtenerPorMarca(id_marca)
    if not modelos:
        return 'No se encontraron modelos para esta marca', 404
    return jsonify([modelo.serialize() for modelo in modelos])
