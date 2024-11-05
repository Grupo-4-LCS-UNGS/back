from flask import Blueprint, request, session, url_for, jsonify
from extensiones import db, bcrypt
from validaciones import *
from models.usuario import Usuario
from flask_login import login_user, logout_user, login_required, current_user


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


@usuarios.route('/login', methods=['POST'])
def login():
    nombre = str(request.form['nombre']).strip()
    contrasena = str(request.form['contrasena']).strip()

    print(f"Nombre: {nombre}, Contraseña: {contrasena}")  

    if not (Valida.nombre(nombre) and Valida.contrasena(contrasena)):
        return jsonify(error='Formato incorrecto', estado=400), 400

    personal = Usuario.buscar(nombre)
    if not personal or not bcrypt.check_password_hash(personal.contrasena, contrasena):
        return jsonify(error='Credenciales incorrectas', estado=400), 400

    login_user(personal)

    return jsonify(id=personal.id, nombre=personal.nombre, rol=personal.rol, estado=200), 200



#endpoint de log out
@usuarios.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('rol', None)
