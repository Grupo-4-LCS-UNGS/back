from sqlalchemy.orm import Mapped, mapped_column, relationship
from database2 import db2

class MarcaVehiculo(db2.Model):
    id:     Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    logo:   Mapped[str]

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'logo': self.logo
        }
