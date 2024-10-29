from flask import Blueprint, request, session, url_for, jsonify
from extensiones import db, bcrypt
from validaciones import *
from models.usuario import Usuario

usuarios = Blueprint('usuarios', __name__)

@usuarios.route('/signin', methods=['POST'])
def signin():
    nombre = str(request.form['nombre']).strip()
    contrasena = str(request.form['contrasena']).strip()
    rol = str(request.form['rol']).strip()

    # Validar que el nombre y la contraseña no estén vacíos
    if not nombre or not contrasena:
        return jsonify(error='datos inválidos', estado=400), 400

    # Verificar si el usuario ya existe
    repetido = Usuario.buscar(nombre)
    if repetido is not None:
        return jsonify(error='usuario ya ingresado', estado=400), 400

    # Crear el usuario
    encriptado = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    respuesta = Usuario.agregar(nombre, encriptado, rol)

    return jsonify(id=respuesta, estado=200), 200


#endpoint de login
@usuarios.route('/login', methods=['POST'])
def inicio():
    #capturamos los datos 
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])

    #validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        personal = Usuario.buscar(nombre)

        verificacion = bcrypt.check_password_hash(personal.contrasena, contrasena)

        # aca verifica la contraseña, si coincide guarda datos
        if verificacion:
            session['user_id'] = personal.id
            session['rol'] = personal.rol
            
            jsonify(id= personal.id, nombre= personal.nombre, rol= personal.rol, estado= 200)
                    
        else:
            jsonify(error= 'contraseña incorrecta', estado= 400)

#endpoint de log out
@usuarios.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('rol', None)
