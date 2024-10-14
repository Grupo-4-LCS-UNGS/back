from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from main import db

class AsignacionRepuestos(db.Model):
    id_mantenimiento: Mapped[int] = mapped_column(ForeignKey('mantenimiento.id'), primary_key=True,nullable=False)
    id_repuesto:      Mapped[int] = mapped_column(ForeignKey('repuesto.id'), primary_key=True, nullable=False)