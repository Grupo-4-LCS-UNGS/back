from datetime import datetime
from sqlalchemy import ForeignKey, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.usuario import Usuario

class BitacoraSolicitudCliente(db.Model):
    id:                Mapped[int] = mapped_column(primary_key=True)
    id_operador:       Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    fecha_hora_inicio: Mapped[datetime] = mapped_column(Date, default=func.now())
    ubicacion_inicio:  Mapped[float]
    fecha_hora_fin:    Mapped[datetime]
    ubicacion_fin:     Mapped[float]

    operador:          Mapped['Usuario'] = relationship('Usuario', backref='solicitudes')

    def serialize(self):
        return {
            'id': self.id,
            'fecha_hora_inicio': self.fecha_hora_inicio,
            'ubicacion_inicio': self.ubicacion_inicio,
            'fecha_hora_fin': self.fecha_hora_fin,
            'ubicacion_fin': self.ubicacion_fin,
            'operador': self.operador.serialize() if self.operador else None
        }

    @staticmethod
    def listar():
        return BitacoraSolicitudCliente.query.all()

    @staticmethod
    def listar_json():
        return [solicitud.serialize() for solicitud in BitacoraSolicitudCliente.listar()]

    @staticmethod
    def agregar(solicitud):
        db.session.add(solicitud)
        db.session.commit()

    @staticmethod
    def eliminar(solicitud):
        db.session.delete(solicitud)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(BitacoraSolicitudCliente, id)