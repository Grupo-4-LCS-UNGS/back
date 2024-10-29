from flask import Flask
from extensiones import db, bcrypt
from routes.marcas_vehiculos import marcas_vehiculos
from routes.ordenes_compra import ordenes_compras
from routes.proveedores import proveedores

from validaciones import *
from config import Config

from routes.usuarios import usuarios
from routes.vehiculos import vehiculos
from routes.mantenimientos import mantenimientos
from routes.repuestos import repuestos


#instancia de flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET KEY'] = Config.SECRET_KEY

#instancia del ORM
db.init_app(app)

#instancia para encriptar
bcrypt.init_app(app)

#para la creacion de tablas
app.app_context().push()
db.create_all()

#registramos las rutas
app.register_blueprint(usuarios)
app.register_blueprint(vehiculos)
app.register_blueprint(mantenimientos)
app.register_blueprint(repuestos)
app.register_blueprint(marcas_vehiculos)
app.register_blueprint(proveedores)
app.register_blueprint(ordenes_compras)

#ejecucion de la app, camiar cuando este en produccion
if __name__ == '__main__':
    app.run(debug=True)
