from flask import Blueprint, jsonify, request, redirect, url_for

from validaciones import *

from models.vehiculo import Vehiculo
from models.mantenimiento import Mantenimiento

mantenimientos = Blueprint('mantenimientos', __name__)

@mantenimientos.route('/mantenimientos')
def listar_mantenimientos():
    mantenimientos = Mantenimiento.listar_json()
    return jsonify(mantenimientos)

@mantenimientos.route('/mantenimientos/alta')
def cargar_mantenimiento():

    matricula = str(request.form['matricula'])
    tipo = str(request.form['tipo'])
    inicio = str(request.form['inicio'])
    fin = str(request.form['fin'])
    descripcion = str(request.form['descripcion'])

    vehiculo = Vehiculo.encontrarPorPatente(matricula)

    if vehiculo is not None:
        mantenimiento = Mantenimiento(
            id_vehiculo= vehiculo.id,
            fecha_inicio= inicio,
            fecha_fin= fin,
            tipo= tipo,
            descripcion= descripcion
        )
        Mantenimiento.agregar(mantenimiento)

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