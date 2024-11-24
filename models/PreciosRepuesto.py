from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.proveedor import Proveedor
from models.repuesto import Repuesto


class PreciosRepuesto(db.Model):
    id:          Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_proveedor: Mapped[int] = mapped_column(ForeignKey('proveedor.id'))
    id_repuesto:  Mapped[int] = mapped_column(ForeignKey('repuesto.id'))
    costo:        Mapped[float]
    proveedor:    Mapped['Proveedor'] = relationship('Proveedor', backref='precios')
    repuesto:     Mapped['Repuesto'] = relationship('Repuesto', backref='catalogo')

    def serialize(self):
        return {
            'proveedor': self.proveedor.serialize() if self.proveedor else None,
            'repuesto': self.repuesto.serialize() if self.repuesto else None,
            'costo': self.costo,
            'id': self.id
        }

    @staticmethod
    def listar():
        return PreciosRepuesto.query.all()

    @staticmethod
    def listar_json():
        return [precios_repuesto.serialize() for precios_repuesto in PreciosRepuesto.listar()]

    @staticmethod
    def agregar(precios_repuesto):
        db.session.add(precios_repuesto)
        db.session.commit()

    @staticmethod
    def eliminar(precios_repuesto):
        db.session.delete(precios_repuesto)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrarPorId(id_proveedor, id_repuesto):
        return db.session.get(PreciosRepuesto, (id_proveedor, id_repuesto))