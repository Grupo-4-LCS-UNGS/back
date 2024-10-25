from flask import Blueprint, request

from models.marca_vehiculo import MarcaVehiculo

marcas_vehiculos = Blueprint('marcas_vehiculos', __name__)

@marcas_vehiculos.route('/marcas_vehiculos/')
def listar_marcas():
    return MarcaVehiculo.listar_json()

@marcas_vehiculos.route('/marcas_vehiculos/', methods=['POST'])
def alta_marca():
    data = request.get_json()
    MarcaVehiculo.agregar(MarcaVehiculo(**data))
    return MarcaVehiculo.listar_json()

@marcas_vehiculos.route('/marcas_vehiculos/<int:id>', methods=['UPDATE'])
def actualizar_marca(id):
    marca = MarcaVehiculo.encontrarPorId(id)
    if marca == None:
        return 'Marca no encontrada', 404

    data = request.get_json()
    marca.nombre = data.get('nombre', marca.nombre)
    marca.logo = data.get('logo', marca.logo)
    MarcaVehiculo.actualizar()
    return MarcaVehiculo.listar_json()