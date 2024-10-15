from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for

from validaciones import *

from models.vehiculo import Vehiculo

vehiculos = Blueprint('vehiculos', __name__)

#endpoint para listar vehiculos
@vehiculos.route('/listado_vehiculos')
def listar_vehiculos():
    vehiculos = Vehiculo.listar()
    return jsonify(vehiculos)

#endpoint de carga de vehiculo
@vehiculos.route('/vehiculo/alta', methods=['GET', 'POST'])
def cargar_vehiculo():
    if request.method == 'GET':
        return render_template('altaVehiculo.html')
    
    #capturamos los datos
    marca = str(request.form['marca'])
    modelo = str(request.form['modelo'])
    anio = int(request.form['anio'])
    patente = str(request.form['patente'])

    vehiculo = Vehiculo(marca, modelo, patente, anio)

    #deberia hacer verificaciones, al menos sobre patente repetida
    if Valida.patente(patente):
        coincidencia = Vehiculo.encontrarPorPatente(patente)

        if coincidencia is not None:
            flash('Vehiculo ya ingresado', 'message')
        else:
            Vehiculo.agregar(vehiculo)
            flash('Vehiculo ingresado con exito', 'success')

    redirect(url_for('listar_vehiculos'))

#endpoint para modificar vehiculo
@vehiculos.route('/vehiculo/mod', methods=['PUT'])
def mod_vehiculo():
    #capturo los datos
    marca = str(request.form['marca'])
    modelo = str(request.form['modelo'])
    anio = int(request.form['anio'])
    patente = str(request.form['patente'])

    #encuentro la entrada a modificar
    coincidencia = Vehiculo.encontrarPorPatente(patente)

    #actualizo y guardo cambios
    coincidencia.marca = marca
    coincidencia.modelo = modelo
    coincidencia.matricula = patente
    coincidencia.anio = anio
    
    Vehiculo.actualizar()

    return flash('modificado con exito', 'success')

#endpoint para dar de baja un vehiculo
@vehiculos.route('/vehiculo/baja')
def baja_vehiculo():
    pass