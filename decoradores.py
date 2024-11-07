from functools import wraps
from flask_jwt_extended import get_jwt
from flask import jsonify

def requiere_rol(rol_requerido):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            rol = claims.get("rol")  # El rol debería estar en el token
            if rol != rol_requerido:
                return jsonify(error="No tienes permisos para acceder a este recurso"), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator