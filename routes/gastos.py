from datetime import datetime
from flask import Blueprint, jsonify, request, redirect, url_for
from validaciones import *  # Asegúrate de tener tus validaciones definidas
from models.gasto import Gasto  # Asegúrate de importar el modelo Gasto

gastos = Blueprint('gastos', __name__)

@gastos.route('/gastos')
def listar_gastos():
      return Gasto.listar_json()


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
        created_at=datetime.utcnow()  # Establece el valor aquí
    )

    Gasto.agregar(nuevo_gasto)
    return jsonify({"message": "Gasto registrado exitosamente"}), 201

@gastos.route('/gastos/mod/<int:id>', methods=['PUT'])
def mod_gasto(id):
    # Lógica para modificar un gasto por ID
    gasto = Gasto.encontrar_por_id(id)
    if not gasto:
        return jsonify({"error": "Gasto no encontrado"}), 404

    data = request.json
    gasto.categoria = data.get('categoria', gasto.categoria)
    gasto.fecha = data.get('fecha', gasto.fecha)
    gasto.monto = data.get('monto', gasto.monto)
    gasto.proveedor_id = data.get('proveedor_id', gasto.proveedor_id)
    gasto.descripcion = data.get('descripcion', gasto.descripcion)

    Gasto.actualizar()  # Asegúrate de que esto funcione como esperas
    return jsonify({"message": "Gasto actualizado exitosamente"}), 200

@gastos.route('/gastos/baja/<int:id>', methods=['DELETE'])
def baja_gasto(id):
    gasto = Gasto.encontrar_por_id(id)
    if not gasto:
        return jsonify({"error": "Gasto no encontrado"}), 404

    Gasto.eliminar(gasto)
    return jsonify({"message": "Gasto eliminado exitosamente"}), 200
