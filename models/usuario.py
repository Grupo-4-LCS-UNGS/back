from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column
from extensiones import db

class Usuario(db.Model, UserMixin):  
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    contrasena: Mapped[str]
    rol: Mapped[str]

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'rol': self.rol,
        }
    
    @staticmethod
    def agregar(nombre, contrasena, rol):
        usuario = Usuario(
            nombre= nombre,
            contrasena= contrasena,
            rol= rol
        )

        db.session.add(usuario)
        db.session.commit()

        res = usuario.id

        usuario = None

        return res

    @staticmethod
    def buscar(nombre):
        return Usuario.query.filter_by(nombre=nombre).first()
    
    def buscarPorId(id):
        return Usuario.query.get(id)

   
    def is_active(self):
        return True  

    def is_authenticated(self):
        return True  

    def is_anonymous(self):
        return False  

    def get_id(self):
        return str(self.id)  
    
    @staticmethod
    def listar_json():
        return [usuario.serialize() for usuario in Usuario.listar()]
    
    
    @staticmethod
    def obtenerPorRol(rol):
        return Usuario.query.filter_by(rol=rol).all()
    
    
