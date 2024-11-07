from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Date, ForeignKey
from extensiones import db
from models.vehiculo import Vehiculo

class Mantenimiento(db.Model):
    id:           Mapped[int] = mapped_column(primary_key=True)
    id_vehiculo:  Mapped[int] = mapped_column(ForeignKey('vehiculo.id'))
    fecha_inicio: Mapped[datetime.date] = mapped_column(Date)
    fecha_fin:    Mapped[datetime.date] = mapped_column(Date)
    estado:       Mapped[str]
    descripcion:  Mapped[str]
    tipo:         Mapped[str]
    vehiculo:     Mapped['Vehiculo'] = relationship('Vehiculo', backref='mantenimientos')

    def serialize(self):
        return {
            'id': self.id,
            'vehiculo': self.vehiculo.serialize() if self.vehiculo else None,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'estado': self.estado,
            'descripcion':self.descripcion
        }

    @staticmethod
    def listar():
        return Mantenimiento.query.all()

    @staticmethod
    def listar_json():
        return [mantenimiento.serialize() for mantenimiento in Mantenimiento.listar()]

    @staticmethod
    def agregar(mantenimiento):
        db.session.add(mantenimiento)
        db.session.commit()

    @staticmethod
    def eliminar(mantenimiento):
        db.session.delete(mantenimiento)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(Mantenimiento, id)