from database2 import db2
from models.mantenimiento import Mantenimiento

class MantenimientoDao:
    def listar(self):
        return Mantenimiento.query.all()

    def agregar(self, mantenimiento):
        db2.session.add(mantenimiento)
        db2.session.commit()

    def eliminar(self, mantenimiento):
        db2.session.delete(mantenimiento)
        db2.session.commit()

    def actualizar(self):
        db2.session.commit()

    def encontrarPorId(self, id):
        return db2.session.get(Mantenimiento, id)