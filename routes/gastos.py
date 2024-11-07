from datetime import datetime
from flask import Blueprint, jsonify, request, redirect, url_for
from flask_login import login_required
from validaciones import *  
from models.gasto import Gasto  
from decoradores import requiere_rol
from flask_jwt_extended import jwt_required, get_jwt

gastos = Blueprint('gastos', __name__)

@gastos.route('/gastos', methods=['GET'])
@jwt_required()  # Protege la ruta con JWT
@requiere_rol('admin')  # Mantiene la verificación del rol como está
def listar_gastos():
    categoria = request.args.get('categoria')
    fecha = request.args.get('fecha')
    monto = request.args.get('monto', type=float)
    proveedor_id = request.args.get('proveedor_id', type=int)
    descripcion = request.args.get('descripcion')

    query = Gasto.query
    if categoria:
        query = query.filter_by(categoria=categoria)
    if fecha:
        query = query.filter_by(fecha=fecha)
    if monto:
        query = query.filter_by(monto=monto)
    if proveedor_id:
        query = query.filter_by(proveedor_id=proveedor_id)
    if descripcion:
        query = query.filter(Gasto.descripcion.ilike(f"%{descripcion}%"))

    gastos = query.all()
    return jsonify([gasto.serialize() for gasto in gastos])




@gastos.route('/gastos/alta', methods=['POST'])
def cargar_gasto():
    data = request.json

    categoria = str(data.get('categoria'))
    fecha = str(data.get('fecha'))
    monto = float(data.get('monto'))
    proveedor_id = data.get('proveedor_id')
    descripcion = str(data.get('descripcion'))

    if not all([categoria, fecha, monto]):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    nuevo_gasto = Gasto(
        categoria=categoria,
        fecha=fecha,
        monto=monto,
        proveedor_id=proveedor_id,
        descripcion=descripcion,
        created_at=datetime.utcnow()  
    )

    Gasto.agregar(nuevo_gasto)
    return jsonify({"message": "Gasto registrado exitosamente"}), 201

@gastos.route('/gastos/baja/<int:id>', methods=['DELETE'])
def baja_gasto(id):
    gasto = Gasto.encontrar_por_id(id)
    if not gasto:
        return jsonify({"error": "Gasto no encontrado"}), 404

    Gasto.eliminar(gasto)
    return jsonify({"message": "Gasto eliminado exitosamente"}), 200
