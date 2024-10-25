from sqlalchemy.orm import Mapped, mapped_column
from extensiones import db

class MarcaVehiculo(db.Model):
    id:     Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    logo:   Mapped[str]

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'logo': self.logo
        }

    @staticmethod
    def listar():
        return MarcaVehiculo.query.all()

    @staticmethod
    def listar_json():
        return [marca_vehiculo.serialize() for marca_vehiculo in MarcaVehiculo.listar()]

    @staticmethod
    def agregar(marca_vehiculo):
        db.session.add(marca_vehiculo)
        db.session.commit()

    @staticmethod
    def eliminar(marca_vehiculo):
        db.session.delete(marca_vehiculo)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(MarcaVehiculo, id)
