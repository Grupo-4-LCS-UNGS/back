from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from extensiones import db
from models.modelo_vehiculo import ModeloVehiculo
from models.usuario import Usuario

class Vehiculo(db.Model):
    id:         Mapped[int] = mapped_column(primary_key=True)
    id_modelo:  Mapped[int] = mapped_column(ForeignKey('modelo_vehiculo.id'))
    id_operador:Mapped[int] = mapped_column(ForeignKey('usuario.id'), nullable=True)
    matricula:  Mapped[str] = mapped_column(unique=True, nullable=False)
    id_traccar: Mapped[int] = mapped_column(nullable=True)
    estado:     Mapped[str] = mapped_column(nullable=True)
    modelo:     Mapped['ModeloVehiculo'] = relationship('ModeloVehiculo', backref='vehiculos')
    operador:   Mapped['Usuario'] = relationship('Usuario', backref='vehiculo')
    kilometraje:Mapped[int] = mapped_column(nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'modelo': self.modelo.serialize() if self.modelo else None,
            'operador': self.operador.serialize() if self.operador else None,
            'matricula': self.matricula,
            'id_traccar': self.id_traccar,
            'estado': self.estado,
            'kilometraje': self.kilometraje,
        }

    @staticmethod
    def listar():
        return Vehiculo.query.all()

    @staticmethod
    def listar_json():
        return [vehiculo.serialize() for vehiculo in Vehiculo.listar()]

    @staticmethod
    def agregar(vehiculo):
        db.session.add(vehiculo)
        db.session.commit()

    @staticmethod
    def eliminar(vehiculo):
        db.session.delete(vehiculo)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return Vehiculo.query.get(id)

    @staticmethod
    def encontrarPorPatente(patente):
        return Vehiculo.query.filter_by(matricula= patente).first()