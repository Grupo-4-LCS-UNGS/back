from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.cliente import Cliente

class PosicionCliente(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey('cliente.id'))
    latitud: Mapped[float]
    longitud: Mapped[float]
    nombre: Mapped[str]

    cliente: Mapped['Cliente'] = relationship('Cliente', backref='posiciones')

    def serialize(self):
        return {
            'id': self.id,
            'id_cliente': self.id_cliente,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'nombre': self.nombre,
            'cliente': self.cliente.serialize() if self.cliente else None
        }

    @staticmethod
    def listar():
        return PosicionCliente.query.all()

    @staticmethod
    def listar_json():
        return [posicion.serialize() for posicion in PosicionCliente.listar()]

    @staticmethod
    def agregar(posicion):
        db.session.add(posicion)
        db.session.commit()

    @staticmethod
    def eliminar(posicion):
        db.session.delete(posicion)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(PosicionCliente, id)