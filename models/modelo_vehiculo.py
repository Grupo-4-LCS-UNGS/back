from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.marca_vehiculo import MarcaVehiculo

class ModeloVehiculo(db.Model):
    id:                 Mapped[int] =   mapped_column(primary_key=True)
    id_marca_vehiculo:  Mapped[int] = mapped_column(ForeignKey('marca_vehiculo.id'))
    nombre:             Mapped[str]
    marca:              Mapped['MarcaVehiculo'] = relationship('MarcaVehiculo', backref='modelos')

    def serialize(self):
        return {
            'id': self.id,
            'marca_vehiculo': self.marca.serialize() if self.marca else None,
            'nombre': self.nombre
        }

    @staticmethod
    def listar():
        return ModeloVehiculo.query.all()

    @staticmethod
    def listar_json():
        return [modelo_vehiculo.serialize() for modelo_vehiculo in ModeloVehiculo.listar()]

    @staticmethod
    def agregar(modelo_vehiculo):
        db.session.add(modelo_vehiculo)
        db.session.commit()

    @staticmethod
    def eliminar(modelo_vehiculo):
        db.session.delete(modelo_vehiculo)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(ModeloVehiculo, id)