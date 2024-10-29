#from main import db
from sys import exception

from psycopg2 import connect, OperationalError, errorcodes, extensions

from config import Config

# from models.asignacion_repuestos import AsignacionRepuestos
# from models.mantenimiento import Mantenimiento
# from models.marca_vehiculo import MarcaVehiculo
# from models.modelo_vehiculo import ModeloVehiculo
# from models.repuesto import Repuesto
# from models.vehiculo import Vehiculo

def crear_base():
    base = abrir_conexion('postgres')

    cur = base.cursor()

    try:
        cur.execute(f'DROP DATABASE IF EXISTS {Config.DB}')
        cur.execute(f'CREATE DATABASE {Config.DB}')

    except OperationalError as err:
        if err.pgerror == errorcodes.DUPLICATE_DATABASE:
            pass

    cur.close()

    base.close()

def crear_tablas():
    base = abrir_conexion(Config.DB)
    cur = base.cursor()

    with open('tablas.sql', 'r') as file:
        sql = file.read()
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        base.close()

def abrir_conexion(db_nombre):
    base = connect(host=Config.HOST,
                   port=Config.PORT,
                   user=Config.USER,
                   password=Config.PASSWORD,
                   database=db_nombre)  # Config.DB)
    base.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    return base

def crearTriggers():
    base = abrir_conexion(Config.DB)
    cur = base.cursor()

    with open('trigger_orden_compra.sql', 'r') as file:
        sql = file.read()
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        base.close()

if __name__ == '__main__':
    crear_base() #esto instancia crea la base de datos
    crear_tablas() #esto crea las tablas
    crearTriggers()
    #db.drop_all() #esto borra las tablas
    #db.create_all() #esto las crea nuevamente
