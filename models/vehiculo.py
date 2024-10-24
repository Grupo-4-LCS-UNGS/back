from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from extensiones import db
from models.modelo_vehiculo import ModeloVehiculo


class Vehiculo(db.Model):
    id:         Mapped[int] = mapped_column(primary_key=True)
    id_modelo:  Mapped[int] = mapped_column(ForeignKey('modelo_vehiculo.id'), nullable=False)
    matricula:  Mapped[str]
    id_traccar: Mapped[int]
    estado:     Mapped[str]
    modelo:     Mapped['ModeloVehiculo'] = relationship('ModeloVehiculo', backref='vehiculos')

    def serialize(self):
        return {
            'id': self.id,
            'modelo': self.modelo.serialize(),
            'matricula': self.matricula,
            'id_traccar': self.id_traccar,
            'estado': self.estado
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
        return db.session.get(Vehiculo, id)

    @staticmethod
    def encontrarPorPatente(patente):
        return Vehiculo.query.filter_by(patente= patente).first()