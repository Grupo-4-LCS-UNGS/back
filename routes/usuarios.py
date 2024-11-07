from flask import Blueprint, request, session, url_for, jsonify
from extensiones import db, bcrypt
from validaciones import *
from models.usuario import Usuario
from flask_login import login_user, logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta

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

    # Genera el token JWT con el rol del usuario incluido en los claims adicionales
    access_token = create_access_token(
        identity=personal.id, 
        expires_delta=timedelta(hours=1),
        additional_claims={"rol": personal.rol}  # Agrega el rol aquí
    )

    # Devuelve el token JWT en la respuesta
    return jsonify(access_token=access_token, id=personal.id, nombre=personal.nombre, rol=personal.rol, estado=200), 200



#endpoint de log out
@usuarios.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('rol', None)

@usuarios.route('/mi_perfil', methods=['GET'])
@jwt_required()
def mi_perfil():

    usuario_id = get_jwt_identity()
    claims = get_jwt()

    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return jsonify(error="Usuario no encontrado"), 404

    return jsonify({
        "nombre": usuario.nombre,
        "rol": claims.get("rol") 
    }), 200