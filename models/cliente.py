from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from extensiones import db

class Cliente(db.Model):
    id:         Mapped[int] = mapped_column(primary_key=True)
    id_operador:Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=True)
    cuit:       Mapped[int] = mapped_column(unique=True)
    nombre:     Mapped[str] = mapped_column(nullable=True)
    direccion:  Mapped[str] = mapped_column(nullable=True)
    email:      Mapped[str] = mapped_column(nullable=True)
    telefono:   Mapped[str] = mapped_column(nullable=True)
    usuario_cliente:    Mapped[str] = mapped_column(nullable=True)
    contrasena: Mapped[str] = mapped_column(nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'cuit': self.cuit,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'email': self.email,
            'telefono': self.telefono,
            'usuario_cliente': self.usuario_cliente,
            'contrasena': self.contrasena
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