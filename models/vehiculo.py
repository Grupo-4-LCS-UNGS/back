from datetime import datetime
from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from database2 import db2
from models.modelo_vehiculo import ModeloVehiculo
from models.sede import Sede

class Vehiculo(db2.Model):
    id:        Mapped[int] = mapped_column(primary_key=True)
    id_modelo: Mapped[int] = mapped_column(ForeignKey('modelo_vehiculo.id'), nullable=False)
    id_sede:   Mapped[int] = mapped_column(ForeignKey('sede.id'), nullable=False)
    matricula: Mapped[str]
    anio:      Mapped[datetime.date] = mapped_column(Date)
    modelo:    Mapped['ModeloVehiculo'] = relationship('ModeloVehiculo', backref='autos')
    sede:      Mapped['Sede'] = relationship('Sede', backref='autos')

    def serialize(self):
        return {
            'id': self.id,
            'id_modelo': self.id_modelo,
            'id_sede': self.id_sede,
            'matricula': self.matricula,
            'anio': self.anio.strftime('%Y-%m-%d')
        }