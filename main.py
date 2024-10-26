from flask import Flask
from extensiones import db, bcrypt

from validaciones import *
from config import Config

from routes.usuarios import usuarios
from routes.vehiculos import vehiculos
from routes.mantenimientos import mantenimientos

#instancia de flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = Config.SECRET_KEY

#instancia del ORM
db.init_app(app)

#instancia para encriptar
bcrypt.init_app(app)

#registramos las rutas
app.register_blueprint(usuarios)
app.register_blueprint(vehiculos)
app.register_blueprint(mantenimientos)

with app.app_context():
    db.drop_all()
    db.create_all() 

#ejecucion de la app, camiar cuando este en produccion
if __name__ == '__main__':
    app.run(debug=True)
