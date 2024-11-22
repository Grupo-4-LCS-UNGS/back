from venv import logger
from flask import Blueprint, jsonify, request
from models.usuario import Usuario
from models.vehiculo import Vehiculo
from models.bitacora_asignaciones import BitacoraAsignaciones
import os
import requests

asig_operador_vehiculo = Blueprint('asig_operador_vehiculo', __name__)

@asig_operador_vehiculo.route('/asignacion', methods=['POST'])
def asignar():
    id_vehiculo = request.form.get('id_vehiculo')
    id_usuario = request.form.get('id_usuario')
    
    
    traccar_api = os.getenv('TRACCAR_API')

    # Obtener información del dispositivo
    devices_response = requests.get(f"{traccar_api}/devices?uniqueId={id_vehiculo}")
    devices = devices_response.json()

    print(devices_response)
    logger.debug(devices_response)
    device = devices[0]

    # Obtener información de la posición del dispositivo
    positions_response = requests.get(f"{traccar_api}/positions?id={device['positionId']}")
    positions = positions_response.json()

    # Encontrar la posición del dispositivo
    position = next((p for p in positions if p['deviceId'] == device['id']), None)
    if not position:
        return jsonify({"error": "Position not found"}), 404

    # Obtener la distancia total
    distancia_inicial = position['attributes'].get('totalDistance', 0.0)
    
    

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
   
    
    
    bitacora = BitacoraAsignaciones.encontrarPorId(int(id_asignacion))
    
    traccar_api = os.getenv('TRACCAR_API')

    # Obtener información del dispositivo
    devices_response = requests.get(f"{traccar_api}/devices?uniqueId={bitacora.vehiculo.id}")
    devices = devices_response.json()

    # Encontrar el dispositivo con el uniqueId igual al id_vehiculo
    device = next((d for d in devices if d['uniqueId'] == bitacora.vehiculo.id), None)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    # Obtener información de la posición del dispositivo
    positions_response = requests.get(f"{traccar_api}/positions?id={device['positionId']}")
    positions = positions_response.json()

    # Encontrar la posición del dispositivo
    position = next((p for p in positions if p['deviceId'] == device['id']), None)
    if not position:
        return jsonify({"error": "Position not found"}), 404

    # Obtener la distancia total
    distancia_final = position['attributes'].get('totalDistance', 0.0)
    
    
    
    
    
    
    
    BitacoraAsignaciones.agregarFechaHoraDesasignacion(int(id_asignacion), float(distancia_final))
    
    return bitacora.serialize(), 201


# Obtener todas las asignaciones
@asig_operador_vehiculo.route('/asignaciones', methods=['GET'])
def obtener_asignaciones():
    asignaciones = BitacoraAsignaciones.listar_json()
    return jsonify(asignaciones)
