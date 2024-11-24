from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.modelo_vehiculo import ModeloVehiculo

class Repuesto(db.Model):
    id:                 Mapped[int] = mapped_column(primary_key=True)
    id_modelo_vehiculo: Mapped[int] = mapped_column(ForeignKey('modelo_vehiculo.id'))
    nombre:             Mapped[str]
    stock:              Mapped[int] #cambie el tipo de dato ya que no guardaba el dato indicado
    umbral_minimo:      Mapped[int]
    umbral_maximo:      Mapped[int]
    modelo_vehiculo:    Mapped['ModeloVehiculo'] = relationship('ModeloVehiculo', backref='repuestos')

    def serialize(self):
        return {
            'id': self.id,
            'modelo_vehiculo': self.modelo_vehiculo.serialize() if self.modelo_vehiculo else None,
            'nombre': self.nombre,
            'stock': self.stock,
            'umbral_minimo': self.umbral_minimo,
            'umbral_maximo': self.umbral_maximo
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
    
    @staticmethod
    def encontrarRepuestosporModelo(id_modelo):
        return Repuesto.query.filter_by(id_modelo_vehiculo=id_modelo).all()