from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from validaciones import *
from config import Config

from dao.vehiculoDao import VehiculoDao
from models.vehiculo import Vehiculo

#instancia de flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET KEY'] = Config.SECRET_KEY

#instancia para encriptar
flask_bcrypt = Bcrypt(app)

#instancia del ORM
db = SQLAlchemy(app)

#endpoint de la pagina principal
@app.route('/')
def index():
    return render_template('index.html')

#endpoint de login
@app.route('/login', methods=['GET', 'POST'])
def inicio():
    if request.method == 'GET':
        return render_template('login.html')
    
    #capturamos los datos 
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])

    #validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        personal = db.buscar_personal(nombre)

        verificacion = flask_bcrypt.check_password_hash(personal['contrasena'], contrasena)

        # aca verifica la contraseña, si coincide guarda datos
        if verificacion:
            session['user_id'] = personal['id']
            session['rol'] = personal['rol']

            #aca redirige segun el rol asignado
            rol = personal['rol']
            ruta = None
            
            match rol:
                case 'Administrador':
                    ruta = 'administracion'
                case 'Operador':
                    ruta = 'operaciones'
                case 'Supervisor':
                    ruta = 'supervision'
                case 'Gerente':
                    ruta = 'Gerente'
                case 'OpMantenimiento':
                    ruta = 'mantenimiento'
                case 'Cliente':
                    ruta = 'principal'

            flash('Login exitoso', 'success')

            return redirect(url_for(ruta))
        
        else:
            flash('Datos incorrectos', 'message')

            return redirect(url_for('login'))
        
@app.route('/principal')
def principal():
    return render_template('principal.html')

#endpoint de sign in
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('/signin.html')

    #capturamos los datos
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])
    rol = str(request.form['rol'])

    #validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        repetido = db.buscar_personal(nombre)

        if repetido is not None:
            flash('usuario existente', 'message')
            return redirect(url_for('signin'))
        else:
            encriptado = flask_bcrypt.generate_password_hash(contrasena).decode('utf-8')
            db.alta_personal(nombre, encriptado, rol)
            flash('Usuario dado de alta', 'success')
            return redirect(url_for('inicio'))

#endpoint de log out
@app.route('logout')
def logout():
    session.pop('user_id', None)
    session.pop('rol', None)

    flash('Sesion cerrada con exito', 'success')

    return redirect(url_for('index'))

#endpoint para listar vehiculos
@app.route('/vehiculos')
def listar_vehiculos():
    vehiculos = VehiculoDao.listar()
    return jsonify(vehiculos)

#endpoint de carga de vehiculo
@app.route('/vehiculo/alta', methods=['GET', 'POST'])
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
        coincidencia = VehiculoDao.encontrarPorPatente(patente)

        if coincidencia is not None:
            flash('Vehiculo ya ingresado', 'message')
        else:
            VehiculoDao.agregar(vehiculo)
            flash('Vehiculo ingresado con exito', 'success')

    redirect(url_for('altaVehiculo'))

#endpoint para modificar vehiculo
@app.route('/vehiculo/mod', methods=['PUT'])
def mod_vehiculo():
    #capturo los datos
    marca = str(request.form['marca'])
    modelo = str(request.form['modelo'])
    anio = int(request.form['anio'])
    patente = str(request.form['patente'])

    #encuentro la entrada a modificar
    coincidencia = VehiculoDao.encontrarPorPatente(patente)

    #actualizo y guardo cambios
    coincidencia.marca = marca
    coincidencia.modelo = modelo
    coincidencia.matricula = patente
    coincidencia.anio = anio
    
    VehiculoDao.actualizar()

    return flash('modificado con exito', 'success')

#endpoint para dar de baja un vehiculo
    

#ejecucion de la app, camiar cuando este en produccion
if __name__ == '__main__':
    app.run(debug=True)
