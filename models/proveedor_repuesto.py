from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.proveedor import Proveedor
from models.repuesto import Repuesto


class ProveedorRepuesto(db.Model):
    id_proveedor: Mapped[int] = mapped_column(ForeignKey('proveedor.id'), primary_key=True)
    id_repuesto:  Mapped[int] = mapped_column(ForeignKey('repuesto.id'), primary_key=True)
    costo:        Mapped[float]
    proveedor:    Mapped['Proveedor'] = relationship('Proveedor', backref='provee')
    repuesto:     Mapped['Repuesto'] = relationship('Repuesto', backref='proveedores')

    def serialize(self):
        return {
            'proveedor': self.proveedor,
            'repuesto': self.repuesto,
            'costo': self.costo
        }

    @staticmethod
    def listar():
        return ProveedorRepuesto.query.all()

    @staticmethod
    def listar_json():
        return [proveedor_repuesto.serialize() for proveedor_repuesto in ProveedorRepuesto.listar()]

    @staticmethod
    def agregar(proveedor_repuesto):
        db.session.add(proveedor_repuesto)
        db.session.commit()

    @staticmethod
    def eliminar(proveedor_repuesto):
        db.session.delete(proveedor_repuesto)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id_proveedor, id_repuesto):
        return db.session.get(ProveedorRepuesto, (id_proveedor, id_repuesto))