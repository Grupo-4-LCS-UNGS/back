from flask import Blueprint, request, render_template, session, redirect, flash, url_for
from extensiones import db, bcrypt
from validaciones import *

usuarios = Blueprint('usuarios', __name__)

#endpoint de sign in
@usuarios.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('/signin.html')

    #capturamos los datos
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])
    rol = str(request.form['rol'])

    #validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        repetido = db.buscar_personal(nombre)

        if repetido is not None:
            flash('usuario existente', 'message')
            return redirect(url_for('signin'))
        else:
            encriptado = bcrypt.generate_password_hash(contrasena).decode('utf-8')
            db.alta_personal(nombre, encriptado, rol)
            flash('Usuario dado de alta', 'success')
            return redirect(url_for('inicio'))

#endpoint de login
@usuarios.route('/login', methods=['GET', 'POST'])
def inicio():
    if request.method == 'GET':
        return render_template('login.html')
    
    #capturamos los datos 
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])

    #validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        personal = db.buscar_personal(nombre)

        verificacion = bcrypt.check_password_hash(personal['contrasena'], contrasena)

        # aca verifica la contraseña, si coincide guarda datos
        if verificacion:
            session['user_id'] = personal['id']
            session['rol'] = personal['rol']

            #aca redirige segun el rol asignado
            rol = personal['rol']
            ruta = None
            
            match rol:
                case 'Administrador':
                    ruta = 'administracion'
                case 'Operador':
                    ruta = 'operaciones'
                case 'Supervisor':
                    ruta = 'supervision'
                case 'Gerente':
                    ruta = 'Gerente'
                case 'OpMantenimiento':
                    ruta = 'mantenimiento'
                case 'Cliente':
                    ruta = 'principal'

            flash('Login exitoso', 'success')

            return redirect(url_for(ruta))
        
        else:
            flash('Datos incorrectos', 'message')

            return redirect(url_for('login'))


#endpoint de log out
@usuarios.route('logout')
def logout():
    session.pop('user_id', None)
    session.pop('rol', None)

    flash('Sesion cerrada con exito', 'success')

    return redirect(url_for('index'))
