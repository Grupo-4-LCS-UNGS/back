from flask import Blueprint
from models.usuario import Usuario
from models.vehiculo import Vehiculo

asig_operador_vehiculo = Blueprint('asig_operador_vehiculo', __name__)

@asig_operador_vehiculo.route('/operadores/<string:nombre>/vehiculos/<int:id_vehiculo>/', methods=['PUT'])
def asignar(id_vehiculo, nombre):
    vehiculo = Vehiculo.encontrarPorId(id_vehiculo)
    usuario = Usuario.buscar(nombre)
    if (vehiculo == None or usuario == None
            or vehiculo.estado != 'ACTIVO'
            or vehiculo.id_operador != None):
        return "Vehiculo u Operador no encontrado", 404
    vehiculo.id_operador = usuario.id
    Vehiculo.actualizar()
    return 'OK', 202

@asig_operador_vehiculo.route('/operadores/<string:nombre>/vehiculos/desasign/<int:id_vehiculo>/', methods=['PUT'])
def desasignar(id_vehiculo, nombre):
    vehiculo = Vehiculo.encontrarPorId(id_vehiculo)
    usuario = Usuario.buscar(nombre)
    print(vehiculo.id_operador)
    print(usuario.id)
    if (vehiculo == None or usuario == None
            or vehiculo.estado != 'ACTIVO'
            or vehiculo.id_operador != usuario.id):
        return "Vehiculo u Operador no encontrado", 404
    vehiculo.id_operador = None
    Vehiculo.actualizar()
    return 'OK', 202