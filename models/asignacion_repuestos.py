from datetime import datetime
from sqlalchemy import ForeignKey, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.mantenimiento import Mantenimiento
from models.repuesto import Repuesto


class AsignacionRepuestos(db.Model):
    id:               Mapped[int] = mapped_column(primary_key=True)
    id_mantenimiento: Mapped[int] = mapped_column(ForeignKey('mantenimiento.id'))
    id_repuesto:      Mapped[int] = mapped_column(ForeignKey('repuesto.id'))
    cantidad:         Mapped[int]
    fecha:            Mapped[datetime.date] = mapped_column(Date, default=func.now())
    mantenimiento:    Mapped['Mantenimiento'] = relationship('Mantenimiento', backref='asignaciones_repuestos')
    repuesto:         Mapped['Repuesto'] = relationship('Repuesto', backref='asignaciones_mantenimientos')

    def serialize(self):
        return {
            'id': self.id,
            'manteniento': self.mantenimiento.serialize() if self.mantenimiento else None,
            'repuesto': self.repuesto.serialize() if self.repuesto else None,
            'cantidad': self.cantidad,
            'fecha': self.fecha
        }

    @staticmethod
    def listar():
        return AsignacionRepuestos.query.all()

    @staticmethod
    def listar_json():
        return [asignacion_repuestos.serialize() for asignacion_repuestos in AsignacionRepuestos.listar()]

    @staticmethod
    def agregar(asignacion_repuestos):
        db.session.add(asignacion_repuestos)
        db.session.commit()

    @staticmethod
    def eliminar(asignacion_repuestos):
        db.session.delete(asignacion_repuestos)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(AsignacionRepuestos, id)