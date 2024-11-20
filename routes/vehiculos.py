from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for

from validaciones import *

from models.vehiculo import Vehiculo
from models.modelo_vehiculo import ModeloVehiculo

vehiculos = Blueprint('vehiculos', __name__)

#endpoint para listar vehiculos
@vehiculos.route('/vehiculos')
def listar_vehiculos():
    vehiculos = Vehiculo.listar_json()
    return jsonify(vehiculos)

#endpoint de carga de vehiculo
@vehiculos.route('/vehiculos/alta', methods=['GET', 'POST'])
def cargar_vehiculo():
    if request.method == 'POST':
        modelo_id = int(request.form['modelo'])
        patente = str(request.form['patente'])
        kilometraje = int(request.form['kilometraje'])

        modelo = ModeloVehiculo.encontrarPorId(modelo_id)
        if not modelo:
            flash('Modelo no encontrado', 'error')
            return jsonify({'error': 'Modelo no encontrado'}), 404

        nuevo_vehiculo = Vehiculo(
            modelo=modelo,
            matricula=patente,
            kilometraje=kilometraje
        )

        Vehiculo.agregar(nuevo_vehiculo)

        flash('Vehiculo agregado con exito', 'success')
        return redirect(url_for('vehiculos.listar_vehiculos'))
        return jsonify({
            'id': nuevo_vehiculo.id,
            'modelo': nuevo_vehiculo.modelo.nombre,
            'patente': nuevo_vehiculo.matricula,
            'kilometraje': nuevo_vehiculo.kilometraje
        }), 200

    return render_template('cargar_vehiculo.html')

#endpoint para modificar vehiculo
@vehiculos.route('/vehiculos/mod', methods=['PUT'])
def mod_vehiculo():
    #capturo los datos
   
    modelo = str(request.form['modelo'])
   
    patente = str(request.form['patente'])

    #encuentro la entrada a modificar
    coincidencia = Vehiculo.encontrarPorPatente(patente)

    #actualizo y guardo cambios
   
    coincidencia.modelo = modelo
    coincidencia.matricula = patente
    coincidencia.anio = anio
    

    
    
    Vehiculo.actualizar()

    flash('modificado con exito', 'success')

    redirect(url_for('listar_vehiculos'))

#endpoint para dar de baja un vehiculo
@vehiculos.route('/vehiculos/baja')
def baja_vehiculo():
    patente = request.form['patente']

    unidad = Vehiculo.encontrarPorPatente(patente)

    unidad.estado = 'Baja'

    Vehiculo.actualizar()

    flash('Vehiculo dado de baja', 'success')

    redirect(url_for('listar_vehiculos'))
