from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from main import db

class Repuesto(db.Model):
    id:                 Mapped[int] = mapped_column(primary_key=True)
    id_modelo_vehiculo: Mapped[int] = mapped_column(ForeignKey('modelo_vehiculo.id'), nullable=False)
    nombre:             Mapped[str]
    stock:              Mapped[str]
    umbral_minimo:      Mapped[int]
    modelo_vehiculo:    Mapped['ModeloVehiculo'] = relationship('ModeloVehiculo', backref='repuestos')

    def serialize(self):
        return {
            'id': self.id,
            'modelo_vehiculo': self.modelo_vehiculo.serialize(),
            'nombre': self.nombre,
            'stock': self.stock,
            'umbral_minimo': self.umbral_minimo
        }

    @staticmethod
    def listar():
        return Repuesto.query.all()

    @staticmethod
    def agregar(vehiculo):
        db.session.add(vehiculo)
        db.session.commit()

    @staticmethod
    def eliminar(vehiculo):
        db.session.delete(vehiculo)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(Repuesto, id)