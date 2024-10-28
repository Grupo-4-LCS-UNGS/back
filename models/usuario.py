from sqlalchemy.orm import Mapped, mapped_column
from extensiones import db

class Usuario(db.Model):
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
        return Usuario.query.filter_by(nombre = nombre).first()