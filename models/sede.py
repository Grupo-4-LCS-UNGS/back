from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database2 import db2

class Sede(db2.Model):
    id:         Mapped[int] = mapped_column(primary_key=True)
    nombre:     Mapped[str]
    direccion:  Mapped[str]
    latitud:    Mapped[float] = mapped_column(Float)
    longitud:   Mapped[float] = mapped_column(Float)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'direccion': self.direccion,
            'latitud': self.latitud,
            'longitud': self.longitud
        }