from flask import Blueprint, jsonify
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from models.bitacora_asignaciones import BitacoraAsignaciones

asig_operador_vehiculo = Blueprint('asig_operador_vehiculo', __name__)

@asig_operador_vehiculo.route('/asignacion/<int:id_usuario>/vehiculos/<int:id_vehiculo>/km/<float:distancia_inicial>', methods=['PUT'])
def asignar(id_vehiculo, id_usuario, distancia_inicial):
    vehiculo = Vehiculo.encontrarPorId(id_vehiculo)
    usuario = Usuario.buscarPorId(id_usuario)
   
    bitacoraAsignaciones = BitacoraAsignaciones(
        vehiculo=vehiculo,
        usuario=usuario,
        distancia_inicial=distancia_inicial
    )
    BitacoraAsignaciones.agregar(bitacoraAsignaciones)
    
    return bitacoraAsignaciones.serialize(), 201
   
    
    
    

@asig_operador_vehiculo.route('/desasignacion/<int:id_asignacion>/km/<float:distancia_final>', methods=['PUT'])
def desasignar(id_asignacion, distancia_final):
    bitacora = BitacoraAsignaciones.encontrarPorId(id_asignacion)
    BitacoraAsignaciones.agregarFechaHoraDesasignacion(id_asignacion, distancia_final)
    return bitacora.serialize(), 201


# Obtener todas las asignaciones
@asig_operador_vehiculo.route('/asignaciones', methods=['GET'])
def obtener_asignaciones():
    asignaciones = BitacoraAsignaciones.listar_json()
    return jsonify(asignaciones)
