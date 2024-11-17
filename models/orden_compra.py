from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.proveedor import Proveedor
from models.repuesto import Repuesto


class OrdenCompra(db.Model):
    id:           Mapped[int] = mapped_column(primary_key=True)
    id_repuesto:  Mapped[int] = mapped_column(ForeignKey('repuesto.id'))
    id_proveedor: Mapped[int] = mapped_column(ForeignKey('proveedor.id'))
    cantidad:     Mapped[int]
    estado:       Mapped[str]
    repuesto:     Mapped['Repuesto'] = relationship('Repuesto', backref='ordenes_compra')
    proveedor:    Mapped['Proveedor'] = relationship('Proveedor', backref='repuestos')
    def serialize(self):
        return {
            'id': self.id,
            'repuesto': self.repuesto.serialize() if self.repuesto else None,
            'proveedor': self.proveedor.serialize() if self.repuesto else None,
            'cantidad': self.cantidad,
            'estado': self.estado
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