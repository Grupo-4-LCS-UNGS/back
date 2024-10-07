import psycopg2 as db

import psycopg2.extras

import psycopg2.errorcodes

from psycopg2 import OperationalError

from datetime import datetime

class Datos:

    def __init__(self, host, port, user, password, database):
        
        self.mydb = None
        self.cur = None

        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self._abrir_conexion()

        try:
            self.cur.execute(f'USE {database}')

        except OperationalError as err:
            if err.pgerror == psycopg2.errorcodes.DUPLICATE_DATABASE:
                self.cur.execute(f"CREATE DATABASE {database}")
                self.mydb.database = database
            else:
                raise err
            
        self.cur.execute('''CREATE TABLE IF NOT EXISTS personal(
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL,
            contrasena VARCHAR(90) NOT NULL,
            rol VARCHAR(30) NOT NULL)''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS vehiculos(
            id INT AUTO_INCREMENT PRRIMARY KEY,
            marca VARCHAR(30) NOT NULL,
            modelo VARCHAR(30) NOT NULL,
            anio INT NOT NULL,
            tipo VARCHAR(20) NOT NULL,
            patente VARCHAR(10) NOT NULL,
            condicion VARCHAR(20) NOT NULL)''')
        
        self.mydb.commit()

        self._cerrar_conexion()

    def _abrir_conexion(self):
        self.mydb = db.connect(
            host= self.host,
            port= self.port,
            user= self.user,
            password= self.password,
            database= self.database
        )

        self.cur = self.mydb.cursor(cursor_factory= psycopg2.extras.RealDictCursor)

    def _cerrar_conexion(self):
        self.cur.close()
        self.mydb.close()

#METODOS DE PERSONAL
    def alta_personal(self, nombre, contrasena, rol):
        #validamos que no hay personal repetido
        self._abrir_conexion()

        self.cur.execute(f'SELECT COUNT(*) FROM personal WHERE nombre = {nombre} AND rol = {rol}')
        resultado = self.cur.fetchone()

        if resultado['COUNT(*)'] == 0:
            self.cur.execute('INSERT INTO personal(nombre, contrasena, rol) VALUES (%s, %s, %s)', 
                            (nombre, contrasena, rol))
        
        self.mydb.commit()

        self._cerrar_conexion()

    def buscar_personal(self, nombre):
        self._abrir_conexion()

        self.cur.execute(f'SELECT * FROM personal WHERE nombre = {nombre}')

        resultado = self.cur.fetchone()

        self._cerrar_conexion()

        return resultado

#METOOS DE VEHICULOS
    def alta_vehiculo(self, marca, modelo, anio, tipo, patente, condicion):
        self._abrir_conexion()

        self.cur.execute('INSERT INTO vehiculos(marca, modelo, anio, tipo, patente, condicion) VALUES (%s, %s, %s, %s, %s, %s)', 
                        (marca, modelo, anio, tipo, patente, condicion))

        self._cerrar_conexion()

    def mod_vehiculo(self):
        pass

    def baja_vehiculo(self):
        pass

    def listar_vehiculo(self):
        pass

    def consultar_vehiculo(self, patente):
        self._abrir_conexion()

        self.cur.execute(f'SELECT * FROM vehiculos WHERE patente = {patente}')

        resultado = self.cur.fetchone()

        self._cerrar_conexion()

        return resultado