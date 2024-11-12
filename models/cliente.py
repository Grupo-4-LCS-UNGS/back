from sqlalchemy.orm import Mapped, mapped_column
from extensiones import db

class Cliente(db.Model):
    id:         Mapped[int] = mapped_column(primary_key=True)
    cuit:       Mapped[int] = mapped_column(unique=True, nullable=False)
    nombre:     Mapped[str]
    direccion:  Mapped[str]
    email:      Mapped[str]
    telefono:   Mapped[str]

    def serialize(self):
        return {
            'id': self.id,
            'cuit': self.cuit,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'email': self.email,
            'telefono': self.telefono
        }

    @staticmethod
    def listar():
        return Cliente.query.all()

    @staticmethod
    def listar_json():
        return [cliente.serialize() for cliente in Cliente.listar()]

    @staticmethod
    def agregar(cliente):
        db.session.add(cliente)
        db.session.commit()

    @staticmethod
    def eliminar(cliente):
        db.session.delete(cliente)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(Cliente, id)