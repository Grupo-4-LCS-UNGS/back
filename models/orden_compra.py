from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.proveedor import Proveedor
from models.repuesto import Repuesto
from sqlalchemy import DateTime
from datetime import datetime


class OrdenCompra(db.Model):
    id:           Mapped[int] = mapped_column(primary_key=True)
    id_repuesto:  Mapped[int] = mapped_column(ForeignKey('repuesto.id'))
    id_proveedor: Mapped[int] = mapped_column(ForeignKey('proveedor.id'), nullable=True)
    cantidad:     Mapped[int]
    estado:       Mapped[str]
    repuesto:     Mapped['Repuesto'] = relationship('Repuesto', backref='ordenes_compra')
    proveedor:    Mapped['Proveedor'] = relationship('Proveedor', backref='repuestos')
    fecha_recepcion: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    
    def serialize(self):
        return {
            'id': self.id,
            'repuesto': self.repuesto.serialize() if self.repuesto else None,
            'proveedor': self.proveedor.serialize() if self.repuesto else None,
            'cantidad': self.cantidad,
            'estado': self.estado,
            'fecha_creacion': self.fecha_creacion,
            'fecha_recepcion': self.fecha_recepcion
        }

    @staticmethod
    def listar():
        return OrdenCompra.query.all()

    @staticmethod
    def listar_json():
        return [orden_compra.serialize() for orden_compra in OrdenCompra.listar()]

    @staticmethod
    def agregar(orden_compra):
        db.session.add(orden_compra)
        db.session.commit()

    @staticmethod
    def eliminar(orden_compra):
        db.session.delete(orden_compra)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id):
        return db.session.get(OrdenCompra, id)
    
    
    @staticmethod
    def informarRecepcion(id):
        orden_compra = OrdenCompra.encontrarPorId(id)
        orden_compra.fecha_recepcion = datetime.now()
        orden_compra.estado = "Recibido"
        OrdenCompra.actualizar()
        return orden_compra.serialize()