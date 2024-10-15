#from main import db

from psycopg2 import connect, OperationalError, errorcodes, extensions

from config import Config

# from models.asignacion_repuestos import AsignacionRepuestos
# from models.mantenimiento import Mantenimiento
# from models.marca_vehiculo import MarcaVehiculo
# from models.modelo_vehiculo import ModeloVehiculo
# from models.repuesto import Repuesto
# from models.vehiculo import Vehiculo

def crear_base():
    base = connect(host= Config.HOST,
                   port= Config.PORT,
                   user= Config.USER,
                   password= Config.PASSWORD,
                   database= 'postgres')#Config.DB)
    
    base.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cur = base.cursor()

    try:
        cur.execute(f'CREATE DATABASE {Config.DB}')

    except OperationalError as err:
        if err.pgerror == errorcodes.DUPLICATE_DATABASE:
            pass
    
    cur.close()

    base.close()

if __name__ == '__main__':
    crear_base() #esto instancia crea la base de datos
    #db.drop_all() #esto borra las tablas
    #db.create_all() #esto las crea nuevamente
