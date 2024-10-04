from flask import Flask, render_template, request, redirect, url_for, flash, session

from flask_bcrypt import Bcrypt

from validaciones import *

from database import *

from config import Config

#instancia de flask
app = Flask(__name__, template_folder='front/html', static_folder='front/static')

#instancia para encriptar
flask_bcrypt = Bcrypt(app)

#instancia de la base de datos
db = Datos(Config.HOST,
           Config.PORT,
           Config.USER,
           Config.PASSWORD,
           Config.DB)

app.config['SECRET KEY'] = Config.SECRET_KEY

#endpoint de la pagina principal
@app.route('/')
def index():
    return render_template('index.html')

#endpoint de login
@app.route('/login', methods=['GET', 'POST'])
def inicio():
    if request.method == 'GET':
        return render_template('login.html')
    
    #capturamos los datos 
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])

    #validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        personal = db.buscar_personal(nombre)

        verificacion = flask_bcrypt.check_password_hash(personal['contrasena'], contrasena)

        # aca verifica la contraseña, si coincide guarda datos redirige
        if verificacion:
            session['user_id'] = personal['id']
            session['rol'] = personal['rol']

            flash('Login exitoso', 'succes')
            
            return redirect(url_for('principal'))
        
        else:
            flash('Datos incorrectos', 'message')

            return redirect(url_for('login'))
        
@app.route('/principal')
def principal():
    return render_template('principal.html')

#endpoint de sign in
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('/signin.html')

    #capturamos los datos
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])

    #validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        repetido = db.buscar_personal(nombre)

        if repetido['nombre'] == nombre:
            
