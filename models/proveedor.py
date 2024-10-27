from sqlalchemy.orm import Mapped, mapped_column
from extensiones import db

class Proveedor(db.Model):
    id:         Mapped[int] = mapped_column(primary_key=True)
    nombre:     Mapped[str]
    direccion:  Mapped[str]
    telefono:   Mapped[str]
    cuit:       Mapped[str]

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'cuit': self.cuit
        }

    @staticmethod
    def listar():
        return Proveedor.query.all()

    @staticmethod
    def listar_json():
        return [proveedor.serialize() for proveedor in Proveedor.listar()]

    @staticmethod
    def agregar(proveedor):
        db.session.add(proveedor)
        db.session.commit()

    @staticmethod
    def eliminar(proveedor):
        db.session.delete(proveedor)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(Proveedor, id)