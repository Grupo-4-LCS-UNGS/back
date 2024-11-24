from email import header
from venv import logger
from flask import Blueprint, jsonify, request, current_app, url_for
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
    

    vehiculo = Vehiculo.encontrarPorId(int(id_vehiculo))
    vehiculo.estado = "En Transito"
    Vehiculo.actualizar()
    
    

  
    traccar_api = os.getenv('TRACCAR_API')

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic aXR1bGFAbG9nb3MubmV0LmFyOkluVGVyMjJTb2w='
    }

    # Obtener información del dispositivo
    devices_response = requests.get(f"{traccar_api}/devices?uniqueId={id_vehiculo}", headers=headers)
    
    
   

   
   
    
    
    devices = devices_response.json()
    device = devices[0]

    # Obtener información de la posición del dispositivo
    positions_response = requests.get(f"{traccar_api}/positions?id={device['positionId']}", headers=headers)
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
    
        # Llamar a /vehiculos/estadoXid con el id_vehiculo y pasar el estado "En Transito"
   

   
    
    
    bitacora = BitacoraAsignaciones.encontrarPorId(int(id_asignacion))
    
    vehiculo = Vehiculo.encontrarPorId(int(bitacora.vehiculo.id))
    vehiculo.estado = "Disponible"
    Vehiculo.actualizar()
    
    
    
    
    
    traccar_api = os.getenv('TRACCAR_API')
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Basic aXR1bGFAbG9nb3MubmV0LmFyOkluVGVyMjJTb2w='
    }


    # Obtener información del dispositivo
    devices_response = requests.get(f"{traccar_api}/devices?uniqueId={bitacora.vehiculo.id}", headers=headers)
    
    
    
    devices = devices_response.json()
    device = devices[0]
    
    

    # Obtener información de la posición del dispositivo
    positions_response = requests.get(f"{traccar_api}/positions?id={device['positionId']}", headers=headers)
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
