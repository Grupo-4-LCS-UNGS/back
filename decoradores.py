# decoradores.py
from functools import wraps
from flask import request, jsonify
from flask_login import current_user

def requiere_rol(rol_requerido):
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated and current_user.rol == rol_requerido:
                return func(*args, **kwargs)
            return jsonify(error='Acceso no autorizado', estado=403), 403
        return wrapped
    return decorator
