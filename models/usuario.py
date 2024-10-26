from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from extensiones import db

class Usuario(db.Model):
    
    id: Mapped[int] = mapped_column(primary_key=True)  # Campo id como clave primaria
    nombre: Mapped[str] = mapped_column(unique=True, nullable=False)  # Nombre único, no puede ser nulo
    contrasena: Mapped[str] = mapped_column(nullable=False)  # Contraseña, no puede ser nulo
    rol: Mapped[str] = mapped_column(nullable=False)  # Rol, no puede ser nulo

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'rol': self.rol
        }
    @staticmethod
    def listar():
        return Usuario.query.all()

    @staticmethod
    def listar_json():
        return [usuario.serialize() for usuario in Usuario.listar()]

    @staticmethod
    def agregar(usuario):
        db.session.add(usuario)
        db.session.commit()

    @staticmethod
    def eliminar(usuario):
        db.session.delete(usuario)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(Usuario, id)

    @staticmethod
    def encontrarPorNombre(nombre):
        return Usuario.query.filter_by(nombre=nombre).first()
