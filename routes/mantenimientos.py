from flask import Blueprint, jsonify, request, redirect, url_for, current_app
from venv import logger
from datetime import datetime


from validaciones import *

from models.vehiculo import Vehiculo
from models.mantenimiento import Mantenimiento
from models.repuesto import Repuesto
from models.asignacion_repuestos import AsignacionRepuestos
from models.usuario import Usuario
from models.vehiculo import Vehiculo

mantenimientos = Blueprint('mantenimientos', __name__)

@mantenimientos.route('/mantenimientos', methods=['GET'])
def listar_mantenimientos():
    mantenimientos = Mantenimiento.listar_json()
    return jsonify(mantenimientos)

#el endpoint recibe los datos del mantenimiento y los id de los repuestos junto a su cantidad,
#debe verificar que la cantidad no exceda y que el vehiculo este en la flota,
#si pasa la verificacion debe generar el registro del mantenimiento,
#el registro de repuestos y el registro de asignacion de repuestos
@mantenimientos.route('/mantenimientos/alta', methods=['POST'])
def cargar_mantenimiento():

    current_app.logger.info('Cargando mantenimiento')
    current_app.logger.debug(request.json)

    data = request.json
    id_vehiculo = data['id_vehiculo']
    tipo = str(data['tipo'])
    inicio = str(data['fecha_inicio'])
    fin = str(data['fecha_fin']) if 'fecha_fin' in data else None 
    
    if fin == "":
        fin = None
        
    
    id_usuario = data['id_usuario']   

    repuestos = data['repuestos']

    #supongo que en el form se carga una lista de los repuestos con su id y su cantidad, 
    # cada uno como dict
    
    # No supongas, documentalo y comunicalo al resto de tu equipo (nt)
    #repuestos = request.form['repuestos']
    
    usuario = Usuario.buscarPorId(id_usuario)

    vehiculo = Vehiculo.encontrarPorId(id_vehiculo)
    vehiculo.estado = "En mantenimiento"
    vehiculo.operador = usuario
    Vehiculo.actualizar()
    
    current_app.logger.info('Vehiculo de form:')
    current_app.logger.debug(data['id_vehiculo'])
    current_app.logger.info('Vehiculo de modelo:')
    current_app.logger.debug(vehiculo)
    

    
    mantenimiento = None

    #agrego la entrada del mantenimiento si es parte de la flota
    if vehiculo is not None:
        mantenimiento = Mantenimiento(
            id_vehiculo= vehiculo.id,
            fecha_inicio= inicio,
            fecha_fin= fin,
            tipo= tipo,
            id_usuario= id_usuario
        )
        Mantenimiento.agregar(mantenimiento)
        
        

    #me fijo si el mantenimiento se cargo con exito para impactar en la asignacion de repuestos
    if mantenimiento is not None:
        for repuesto in repuestos:
            
            #convertir el id a int
            
            producto = Repuesto.encontrarPorId(int(repuesto['id']))
            asignacion = AsignacionRepuestos(
                id_mantenimiento=mantenimiento.id,
                id_repuesto=producto.id,
                cantidad=repuesto['cantidad']
            )
            AsignacionRepuestos.agregar(asignacion)

            #aca debe actualizar el stock
            producto.stock -= repuesto['cantidad']
            Repuesto.actualizar()
    
    else:
        current_app.logger.error('No se pudo cargar el mantenimiento')
        return "No se pudo cargar el mantenimiento", 400
        

    return jsonify(mantenimiento.serialize()), 201

@mantenimientos.route('/mantenimientos/mod')
def mod_mantenimiento():
    pass

@mantenimientos.route('/mantenimientos/baja')
def baja_mantenimiento():
    pass

@mantenimientos.route('/mantenimientos/<int:id>')
def historial_vehiculo(id):
    resultado = []
    mantenimientos = Mantenimiento.listar()
    for mantenimiento in mantenimientos:
        if mantenimiento.id_vehiculo == id:
            resultado.append(mantenimiento.serialize())

    return resultado, 200


@mantenimientos.route('/mantenimientos/finalizar/<int:id>', methods=['GET'])
def finalizar_mantenimiento(id):
    mantenimiento = Mantenimiento.encontrarPorId(id)
    if mantenimiento is None:
        return 'Mantenimiento no encontrado', 404
    mantenimiento.fecha_fin = datetime.now()
    mantenimiento.estado = 'finalizado'
    
    vehiculo = Vehiculo.encontrarPorId(mantenimiento.id_vehiculo)
    vehiculo.estado = "Disponible"
    vehiculo.operador = None
    Vehiculo.actualizar()
    
    
    Mantenimiento.actualizar()
    return 'OK', 202