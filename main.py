from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from validaciones import *
from config import Config

from routes.usuarios import usuarios
from routes.vehiculos import vehiculos

from models.vehiculo import Vehiculo

#instancia de flask
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET KEY'] = Config.SECRET_KEY

#instancia para encriptar
flask_bcrypt = Bcrypt(app)

#instancia del ORM
db = SQLAlchemy(app)

#registramos las rutas
app.register_blueprint(usuarios)
app.register_blueprint(vehiculos)

#endpoint vistas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/principal')
def principal():
    return render_template('principal.html')

#ejecucion de la app, camiar cuando este en produccion
if __name__ == '__main__':
    app.run(debug=True)
