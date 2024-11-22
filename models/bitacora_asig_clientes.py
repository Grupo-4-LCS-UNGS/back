from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.cliente import Cliente
from models.usuario import Usuario
from models.vehiculo import Vehiculo

class BitacoraAsigClientes(db.Model):
    id:                       Mapped[int] = mapped_column(primary_key=True)
    id_cliente:               Mapped[int] = mapped_column(ForeignKey('cliente.id'))
    id_operador:              Mapped[int] = mapped_column(ForeignKey('usuario.id'))
    id_vehiculo:              Mapped[int] = mapped_column(ForeignKey('vehiculo.id'))
    fecha_hora_asignacion:    Mapped[datetime] = mapped_column(default=func.now())
    fecha_hora_desasignacion: Mapped[datetime] = mapped_column(nullable=True)

    cliente: Mapped['Cliente'] = relationship('Cliente', backref='asig_operadores')
    operador: Mapped['Usuario'] = relationship('Usuario', backref='asig_clientes')
    vehiculo: Mapped['Vehiculo'] = relationship('Vehiculo', backref='bit_asig')

    def serialize(self):
        return {
            'id': self.id,
            'fecha_hora_asignacion': self.fecha_hora_asignacion,
            'fecha_hora_desasignacion': self.fecha_hora_desasignacion,
            'cliente': self.cliente.serialize() if self.cliente else None,
            'operador': self.operador.serialize() if self.operador else None,
            'vehiculo': self.vehiculo.serialize() if self.vehiculo else None
        }

    @staticmethod
    def listar():
        return BitacoraAsigClientes.query.all()

    @staticmethod
    def listar_json():
        return [asignacion.serialize() for asignacion in BitacoraAsigClientes.listar()]

    @staticmethod
    def agregar(asignacion):
        db.session.add(asignacion)
        db.session.commit()

    @staticmethod
    def eliminar(asignacion):
        db.session.delete(asignacion)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(BitacoraAsigClientes, id)