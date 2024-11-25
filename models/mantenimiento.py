from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Date, ForeignKey
from extensiones import db
from models.vehiculo import Vehiculo
from models.usuario import Usuario

class Mantenimiento(db.Model):
    id:           Mapped[int] = mapped_column(primary_key=True)
    id_vehiculo:  Mapped[int] = mapped_column(ForeignKey('vehiculo.id'))
    fecha_inicio: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    fecha_fin:    Mapped[datetime.date] = mapped_column(Date, nullable=True)
    tipo:         Mapped[str] = mapped_column(nullable=True)
    vehiculo:     Mapped['Vehiculo'] = relationship('Vehiculo', backref='mantenimientos')
    id_usuario:   Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    usuario:      Mapped['Usuario'] = relationship('Usuario', backref='mantenimientos')

    def serialize(self):
        return {
            'id': self.id,
            'vehiculo': self.vehiculo.serialize() if self.vehiculo else None,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'tipo': self.tipo,
            'usuario': self.usuario.serialize() if self.usuario else None
        }

    @staticmethod
    def listar():
        #retornar pero ordenando el id de manera descendente
        return Mantenimiento.query.order_by(Mantenimiento.id.desc()).all()
        

    @staticmethod
    def listar_json():
        return [mantenimiento.serialize() for mantenimiento in Mantenimiento.listar()]

    @staticmethod
    def agregar(mantenimiento):
        db.session.add(mantenimiento)
        db.session.commit()

    @staticmethod
    def eliminar(mantenimiento):
        db.session.delete(mantenimiento)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(Mantenimiento, id)
    
    