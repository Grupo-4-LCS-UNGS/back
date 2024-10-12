from main import db
from models.vehiculo import Vehiculo

class VehiculoDao:
    def listar(self):
        return Vehiculo.query.all()

    def agregar(self, vehiculo):
        db.session.add(vehiculo)
        db.session.commit()

    def eliminar(self, vehiculo):
        db.session.delete(vehiculo)
        db.session.commit()

    def actualizar(self):
        db.session.commit()

    def encontrarPorId(self, id):
        return db.session.get(Vehiculo, id)
    
    def encontrarPorPatente(self, patente):
        return Vehiculo.query.filter_by(patente= patente).first()
    