from datetime import datetime
from sqlalchemy import ForeignKey, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from .vehiculo import Vehiculo
from .usuario import Usuario

class BitacoraAsignaciones(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    id_vehiculo: Mapped[int] = mapped_column(ForeignKey('vehiculo.id'))
    id_usuario: Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    fecha_hora_asignacion: Mapped[datetime] = mapped_column(default=func.now())
    fecha_hora_desasignacion: Mapped[datetime] = mapped_column(nullable=True)

    vehiculo: Mapped['Vehiculo'] = relationship('Vehiculo', backref='bitacoras_asignaciones')
    usuario: Mapped['Usuario'] = relationship('Usuario', backref='bitacoras_asignaciones')

    def serialize(self):
        return {
            'id': self.id,
            'vehiculo': self.vehiculo.serialize() if self.vehiculo else None,
            'usuario': self.usuario.serialize() if self.usuario else None,
            'fecha_hora_asignacion': self.fecha_hora_asignacion,
            'fecha_hora_desasignacion': self.fecha_hora_desasignacion,
        }

    @staticmethod
    def agregar(bitacora):
        db.session.add(bitacora)
        db.session.commit()

    @staticmethod
    def listar():
        return BitacoraAsignaciones.query.all()

    @staticmethod
    def listar_json():
        return [bitacora.serialize() for bitacora in BitacoraAsignaciones.listar()]

    @staticmethod
    def encontrarPorId(id):
        return BitacoraAsignaciones.query.get(id)
    
    @staticmethod
    def agregarFechaHoraDesasignacion(id):
        bitacora = BitacoraAsignaciones.encontrarPorId(id)
        bitacora.fecha_hora_desasignacion = func.now()
        db.session.commit()