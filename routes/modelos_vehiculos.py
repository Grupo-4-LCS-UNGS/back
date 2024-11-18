from flask import Blueprint, request

from models.modelo_vehiculo import ModeloVehiculo

modelos_vehiculos = Blueprint('modelos_vehiculos', __name__)

@modelos_vehiculos.route('/modelos_vehiculos/')
def listar_modelos():
    return ModeloVehiculo.listar_json()

@modelos_vehiculos.route('/modelos_vehiculos/', methods=['POST'])
def alta_modelo():
    data = request.get_json()
    ModeloVehiculo.agregar(ModeloVehiculo(**data))
    return 'OK', 202

@modelos_vehiculos.route('/modelos_vehiculos/<int:id>', methods=['PUT'])
def actualizar_marca(id):
    modelo = ModeloVehiculo.encontrarPorId(id)
    if modelo == None:
        return 'Modelo no encontrada', 404

    data = request.get_json()
    modelo.id_marca_vehiculo = data.get('id_marca_vehiculo')
    modelo.nombre = data.get('nombre', modelo.nombre)
    modelo.litrosx100km = data.get('litrosx100km', modelo.litrosx100km)
    ModeloVehiculo.actualizar()
    return 'OK', 202