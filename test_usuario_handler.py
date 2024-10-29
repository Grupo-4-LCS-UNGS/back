import pytest
from flask import json
from main import app, db  # Asegúrate de importar tu aplicación y base de datos
from sqlalchemy import text


@pytest.fixture
def client():
    """Configura una base de datos de prueba y devuelve un cliente de Flask."""
    with app.app_context():
        db.create_all()  # Crea las tablas en la base de datos temporal
        yield app.test_client()  # Devuelve el cliente para realizar solicitudes
        db.session.remove()  # Remueve la sesión actual

        # Elimina las tablas en el orden correcto
        with db.engine.connect() as connection:
            # Primero eliminar las tablas que dependen de otras
            connection.execute(text("DROP TABLE IF EXISTS asignacion_repuestos;"))  # Depende de mantenimiento
            connection.execute(text("DROP TABLE IF EXISTS mantenimiento;"))  # Luego elimina mantenimiento
            connection.execute(text("DROP TABLE IF EXISTS usuarios;"))  # Finalmente elimina otras tablas

        # Alternativamente, puedes usar db.drop_all() si no hay dependencias
"""
def test_signin_crear_usuario(client):
    response = client.post('/signin', data={
        'nombre': 'Usuario Test',
        'contrasena': 'password123',
        'rol': 'admin'
    })
    assert response.status_code == 200
    json_data = json.loads(response.data)
    assert 'id' in json_data
"""

def test_signin_usuario_existente(client):
    client.post('/signin', data={
        'nombre': 'Usuario Existente',
        'contrasena': 'password456',
        'rol': 'user'
    })
    
    response = client.post('/signin', data={
        'nombre': 'Usuario Existente',
        'contrasena': 'password456',
        'rol': 'user'
    })

    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert json_data['error'] == 'usuario ya ingresado'

def test_signin_datos_invalidos(client):
    response = client.post('/signin', data={
        'nombre': '',
        'contrasena': '',
        'rol': 'user'
    })

    assert response.status_code == 400
    json_data = json.loads(response.data)
    assert json_data['error'] == 'datos inválidos'



if __name__ == "__main__":
    pytest.main()
