from flask import Flask
from sqlalchemy import text
from extensiones import db, bcrypt, login_manager, jwt

from routes.asig_operador_vehiculo import asig_operador_vehiculo
from routes.asignaciones_repuestos import asignaciones_repuestos
from routes.bitacora_clientes import bitacora_clientes
from routes.marcas_vehiculos import marcas_vehiculos
from routes.modelos_vehiculos import modelos_vehiculos
from routes.ordenes_compra import ordenes_compras
from routes.proveedores import proveedores
from routes.gastos import gastos
from routes.PreciosRepuesto import proveedores_repuesto
from routes.usuarios import Usuario, usuarios
from routes.vehiculos import vehiculos
from routes.mantenimientos import mantenimientos
from routes.repuestos import repuestos
from routes.clientes import clientes

from setup import crearTriggers
from config import Config
from dotenv import load_dotenv
import os
from colorama import Fore, Back, Style

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = Config.FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = Config.SECRET_KEY

db.init_app(app)

bcrypt.init_app(app)

jwt.init_app(app)

login_manager.init_app(app)  
login_manager.login_view = 'usuarios.login'  

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))  

app.app_context().push()
db.create_all()

app.register_blueprint(usuarios)
app.register_blueprint(vehiculos)
app.register_blueprint(mantenimientos)
app.register_blueprint(repuestos)
app.register_blueprint(marcas_vehiculos)
app.register_blueprint(proveedores)
app.register_blueprint(ordenes_compras)
app.register_blueprint(gastos)
app.register_blueprint(asignaciones_repuestos)
app.register_blueprint(asig_operador_vehiculo)
app.register_blueprint(modelos_vehiculos)
app.register_blueprint(PreciosRepuesto)
app.register_blueprint(clientes)
app.register_blueprint(bitacora_clientes)

def crear_triggers():
    with open('triggers.sql', 'r') as file:
        sql = file.read()

    with db.engine.connect() as conexion:
        conexion.execute(text(sql))

if not os.getenv('ENV'):
    os.environ['ENV'] = 'development'
    env_file = '.env.development'
    load_dotenv(env_file)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        crearTriggers()

    debuggear = True
    if os.getenv('ENV') == 'development':
        app.run(debug=debuggear)
    elif os.getenv('ENV') == 'production':
        debuggear = False

    print(Back.RED + Fore.WHITE + Style.BRIGHT + 'Iniciando el Transportador' + Style.RESET_ALL)
    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + 'Ambiente: ' + os.getenv('ENV') + Style.RESET_ALL)

    app.run(debug=debuggear, port=os.getenv('APP_PORT'), host=os.getenv('APP_HOST'))
