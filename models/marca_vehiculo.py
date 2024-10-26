from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db

class MarcaVehiculo(db.Model):
    id:     Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    logo:   Mapped[str] = mapped_column(nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'logo': self.logo
        }

    @staticmethod
    def encontrar_por_nombre(nombre):
        return MarcaVehiculo.query.filter_by(nombre=nombre).first()