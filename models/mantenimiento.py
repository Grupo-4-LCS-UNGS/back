from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Date, ForeignKey
from database2 import db2
from models.vehiculo import Vehiculo

class Mantenimiento(db2.Model):
    id:           Mapped[int] = mapped_column(primary_key=True)
    id_vehiculo:  Mapped[int] = mapped_column(ForeignKey('vehiculo.id'), nullable=False)
    fecha_inicio: Mapped[datetime.date] = mapped_column(Date)
    tipo:         Mapped[str]
    descripcion:  Mapped[str]
    estado:       Mapped[str]
    vehiculo:     Mapped['Vehiculo'] = relationship('Vehiculo', backref='mantenimiento')

    def serialize(self):
        return {
            'id': self.id,
            'id_vehiculo': self.id_vehiculo,
            'fecha_inicio': self.fecha_inicio,
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'estado': self.estado
        }