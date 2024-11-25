from flask import Blueprint, jsonify, request, redirect, url_for

from validaciones import *

from models.vehiculo import Vehiculo
from models.mantenimiento import Mantenimiento
from models.repuesto import Repuesto
from models.asignacion_repuestos import AsignacionRepuestos

mantenimientos = Blueprint('mantenimientos', __name__)

@mantenimientos.route('/mantenimientos')
def listar_mantenimientos():
    mantenimientos = Mantenimiento.listar_json()
    return jsonify(mantenimientos)

#el endpoint recibe los datos del mantenimiento y los id de los repuestos junto a su cantidad,
#debe verificar que la cantidad no exceda y que el vehiculo este en la flota,
#si pasa la verificacion debe generar el registro del mantenimiento,
#el registro de repuestos y el registro de asignacion de repuestos
@mantenimientos.route('/mantenimientos/alta', methods=['POST'])
def cargar_mantenimiento():

    id_vehiculo = request.form['id_vehiculo']
    tipo = str(request.form['tipo'])
    inicio = str(request.form['fecha_inicio'])
    #la fecha de fin puede no estar definida
    fin = str(request.form['fecha_fin']) if 'fecha_fin' in request.form else None    

    #supongo que en el form se carga una lista de los repuestos con su id y su cantidad, cada uno como dict
    repuestos = request.form['repuestos']

    vehiculo = Vehiculo.encontrarPorId(id_vehiculo)
    mantenimiento = None

    #agrego la entrada del mantenimiento si es parte de la flota
    if vehiculo is not None:
        mantenimiento = Mantenimiento(
            id_vehiculo= vehiculo.id,
            fecha_inicio= inicio,
            fecha_fin= fin,
            tipo= tipo,
        )
        Mantenimiento.agregar(mantenimiento)

    #me fijo si el mantenimiento se cargo con exito para impactar en la asignacion de repuestos
    if mantenimiento is not None:
        for repuesto in repuestos:
            producto = Repuesto.encontrarPorId(repuesto['id'])
            asignacion = AsignacionRepuestos(mantenimiento, producto, stock= repuesto['cantidad'])
            AsignacionRepuestos.agregar(asignacion)

            #aca debe actualizar el stock
            producto.stock -= repuesto['cantidad']
            Repuesto.actualizar()

    redirect(url_for('listar_mantenimientos'))

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