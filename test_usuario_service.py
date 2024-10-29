import pytest
from extensiones import db
from models.usuario import Usuario
from main import app  # Importa la instancia de app directamente
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


def test_agregar_usuario(client):
    """Prueba el método agregar de la clase Usuario."""
    user_id = Usuario.agregar(nombre='Usuario Test', contrasena='password123', rol='admin')

    assert user_id is not None  

    
    usuario = db.session.get(Usuario, user_id) 

    assert usuario is not None  
    assert usuario.nombre == 'Usuario Test'
    assert usuario.rol == 'admin'  

def test_buscar_usuario(client):

    user_id = Usuario.agregar(nombre='Usuario Buscar', contrasena='password456', rol='user')

    assert user_id is not None 

    usuario_buscado = db.session.query(Usuario).filter_by(nombre='Usuario Buscar').first()

    assert usuario_buscado is not None  
    assert usuario_buscado.nombre == 'Usuario Buscar'  
    assert usuario_buscado.rol == 'user' 
    
def test_buscar_usuario_no_existente(client):
    usuario_buscado = Usuario.buscar(nombre='Usuario Inexistente')

    assert usuario_buscado is None  


if __name__ == "__main__":
    pytest.main()
