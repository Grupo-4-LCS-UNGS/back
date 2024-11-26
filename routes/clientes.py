from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required,create_access_token
from extensiones import db, bcrypt
from models.cliente import Cliente
from datetime import timedelta

clientes = Blueprint('clientes', __name__)

# Endpoint para listar todos los clientes
@clientes.route('/clientes', methods=['GET'])
@jwt_required()
def listar_clientes():
    clientes = Cliente.listar_json()
    return jsonify(clientes), 200


# Endpoint para agregar un nuevo cliente
@clientes.route('/clientes', methods=['POST'])
@jwt_required()
def agregar_cliente():
    data = request.json

    cuit = data.get('cuit')
    nombre = data.get('nombre')
    direccion = data.get('direccion')
    email = data.get('email')
    telefono = data.get('telefono')
    usuario_cliente = data.get('usuario_cliente')
    contrasena = data.get('contrasena')
    id_operador = data.get('id_operador')

    # Validación básica de datos obligatorios
    if not cuit or not nombre or not usuario_cliente or not contrasena:
        return jsonify(error='CUIT, Nombre, Usuario y Contraseña son obligatorios'), 400

    # Verificar que el CUIT o el usuario no existan
    if Cliente.query.filter_by(cuit=cuit).first():
        return jsonify(error='CUIT ya registrado'), 400

    if Cliente.query.filter_by(usuario_cliente=usuario_cliente).first():
        return jsonify(error='Usuario ya registrado'), 400

    # Encriptar la contraseña
    contrasena_encriptada = bcrypt.generate_password_hash(contrasena).decode('utf-8')

    # Crear y guardar el cliente
    nuevo_cliente = Cliente(
        cuit=cuit,
        nombre=nombre,
        direccion=direccion,
        email=email,
        telefono=telefono,
        usuario_cliente=usuario_cliente,
        contrasena=contrasena_encriptada,
        id_operador=id_operador
    )
    Cliente.agregar(nuevo_cliente)
    access_token = create_access_token(
        identity=str(nuevo_cliente.id),  # Convertir a cadena
        expires_delta=timedelta(hours=1),
        additional_claims={"usuario_cliente": nuevo_cliente.usuario_cliente}
    )
    return jsonify(nuevo_cliente.serialize(), access_token=access_token), 201


@clientes.route('/clientes/login', methods=['POST'])
def login_cliente():
    data = request.json
    usuario_cliente = data.get('usuario_cliente')
    contrasena = data.get('contrasena')

    # Validar entrada
    if not usuario_cliente or not contrasena:
        return jsonify(error='Usuario y contraseña son requeridos'), 400

    # Buscar cliente por usuario_cliente
    cliente = Cliente.query.filter_by(usuario_cliente=usuario_cliente).first()
    if not cliente:
        return jsonify(error='Credenciales incorrectas'), 401

    # Verificar contraseña
    if not bcrypt.check_password_hash(cliente.contrasena, contrasena):
        return jsonify(error='Credenciales incorrectas'), 401

    # Generar token JWT
    access_token = create_access_token(
        identity=str(cliente.id),  # Convertir a cadena
        expires_delta=timedelta(hours=1),
        additional_claims={"usuario_cliente": cliente.usuario_cliente}
    )

    return jsonify(access_token=access_token, id=cliente.id, nombre=cliente.nombre), 200



# Endpoint para eliminar un cliente por ID
@clientes.route('/clientes/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_cliente(id):
    cliente = Cliente.encontrarPorId(id)
    if not cliente:
        return jsonify(error='Cliente no encontrado'), 404

    Cliente.eliminar(cliente)
    return jsonify(message='Cliente eliminado correctamente'), 200


# Endpoint para actualizar un cliente por ID
@clientes.route('/clientes/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_cliente(id):
    data = request.json
    cliente = Cliente.encontrarPorId(id)

    if not cliente:
        return jsonify(error='Cliente no encontrado'), 404

    cliente.nombre = data.get('nombre', cliente.nombre)
    cliente.direccion = data.get('direccion', cliente.direccion)
    cliente.email = data.get('email', cliente.email)
    cliente.telefono = data.get('telefono', cliente.telefono)
    cliente.usuario_cliente = data.get('usuario_cliente', cliente.usuario_cliente)

    # Encriptar la nueva contraseña si se proporciona
    nueva_contrasena = data.get('contrasena')
    if nueva_contrasena:
        cliente.contrasena = bcrypt.generate_password_hash(nueva_contrasena).decode('utf-8')

    cliente.id_operador = data.get('id_operador', cliente.id_operador)

    Cliente.actualizar()
    return jsonify(cliente.serialize()), 200
