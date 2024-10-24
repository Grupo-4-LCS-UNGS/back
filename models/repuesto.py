from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.modelo_vehiculo import ModeloVehiculo

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
    def listar_json():
        return [repuesto.serialize() for repuesto in Repuesto.listar()]

    @staticmethod
    def agregar(repuesto):
        db.session.add(repuesto)
        db.session.commit()

    @staticmethod
    def eliminar(repuesto):
        db.session.delete(repuesto)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(Repuesto, id)