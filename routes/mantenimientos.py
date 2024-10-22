from flask import Blueprint, jsonify, request, render_template

from models.vehiculo import Vehiculo
from models.mantenimiento import Mantenimiento

mantenimientos = Blueprint('mantenimientos', __name__)

@mantenimientos.route('/mantenimientos')
def listar_mantenimientos():
    mantenimientos = Mantenimiento.listar_json()
    return jsonify(mantenimientos)

@mantenimientos.route('/mantenimientos/alta')
def cargar_mantenimiento():
    if request.method == 'GET':
        return render_template()

@mantenimientos.route('/mantenimientos/mod')
def mod_mantenimiento():
    pass

@mantenimientos.route('/mantenimientos/baja')
def baja_mantenimiento():
    pass