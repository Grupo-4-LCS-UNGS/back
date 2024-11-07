from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.modelo_vehiculo import ModeloVehiculo
from models.proveedor import Proveedor

class Repuesto(db.Model):
    id:                 Mapped[int] = mapped_column(primary_key=True)
    id_proveedor:       Mapped[int] = mapped_column(ForeignKey('proveedor.id'))
    id_modelo_vehiculo: Mapped[int] = mapped_column(ForeignKey('modelo_vehiculo.id'))
    nombre:             Mapped[str]
    stock:              Mapped[int] #cambie el tipo de dato ya que no guardaba el dato indicado
    umbral_minimo:      Mapped[int]
    umbral_maximo:      Mapped[int]
    proveedor:          Mapped['Proveedor'] = relationship('Proveedor', backref='repuestos')
    modelo_vehiculo:    Mapped['ModeloVehiculo'] = relationship('ModeloVehiculo', backref='repuestos')

    def serialize(self):
        return {
            'id': self.id,
            'proveedor': self.proveedor.serialize() if self.proveedor else None,
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