from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensiones import db
from models.proveedor import Proveedor

class Gasto(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    categoria: Mapped[str] = mapped_column()
    fecha: Mapped[str] = mapped_column()
    monto: Mapped[float] = mapped_column()
    proveedor_id: Mapped[int] = mapped_column(ForeignKey('proveedor.id'), nullable=True)
    descripcion: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow) 

    proveedor: Mapped['Proveedor'] = relationship('Proveedor', backref='gasto')

    def serialize(self):
        return {
            'id': self.id,
            'categoria': self.categoria,
            'fecha': self.fecha,
            'monto': float(self.monto),
            'proveedor': self.proveedor.serialize() if self.proveedor else None,
            'descripcion': self.descripcion,
            'created_at': self.created_at.isoformat() if self.created_at else None,  
        }

    


    @staticmethod
    def listar():
        return Gasto.query.all()

    @staticmethod
    def listar_json():
        return [gasto.serialize() for gasto in Gasto.listar()]

    @staticmethod
    def agregar(gasto):
        db.session.add(gasto)
        db.session.commit()

    @staticmethod
    def eliminar(gasto):
        db.session.delete(gasto)
        db.session.commit()

    @staticmethod
    def actualizar():
        db.session.commit()

    @staticmethod
    def encontrar_por_id(id):
        return db.session.get(Gasto, id)
