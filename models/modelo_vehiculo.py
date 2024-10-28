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
            'marca_vehiculo': self.marca.serialize(),
            'nombre': self.nombre
        }