from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from models.bitacora_asignaciones import BitacoraAsignaciones

asig_operador_vehiculo = Blueprint('asig_operador_vehiculo', __name__)

@asig_operador_vehiculo.route('/asignacion', methods=['POST'])
def asignar():
    id_vehiculo = request.form.get('id_vehiculo')
    id_usuario = request.form.get('id_usuario')
    distancia_inicial = request.form.get('distancia_inicial')

    vehiculo = Vehiculo.encontrarPorId(int(id_vehiculo))
    usuario = Usuario.buscarPorId(int(id_usuario))
   
    bitacoraAsignaciones = BitacoraAsignaciones(
        vehiculo=vehiculo,
        usuario=usuario,
        distancia_inicial=float(distancia_inicial)
    )
    BitacoraAsignaciones.agregar(bitacoraAsignaciones)
    
    return bitacoraAsignaciones.serialize(), 201
   
    
    
    

@asig_operador_vehiculo.route('/desasignacion', methods=['POST'])
def desasignar():
    id_asignacion = request.form.get('id_asignacion')
    distancia_final = request.form.get('distancia_final')
    
    bitacora = BitacoraAsignaciones.encontrarPorId(int(id_asignacion))
    BitacoraAsignaciones.agregarFechaHoraDesasignacion(int(id_asignacion), float(distancia_final))
    
    return bitacora.serialize(), 201


# Obtener todas las asignaciones
@asig_operador_vehiculo.route('/asignaciones', methods=['GET'])
def obtener_asignaciones():
    asignaciones = BitacoraAsignaciones.listar_json()
    return jsonify(asignaciones)
