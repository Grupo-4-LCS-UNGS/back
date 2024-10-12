from datetime import datetime
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column
from main import db

class Vehiculo(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    marca: Mapped[str]
    modelo: Mapped[str]
    matricula: Mapped[str]
    anio: Mapped[datetime.date] = mapped_column(Date)

    def serialize(self):
        return {
            'id': self.id,
            'marca': self.marca,
            'modelo': self.modelo,
            'matricula': self.matricula,
            'anio': self.anio.strftime('%Y-%m-%d')
        }
    