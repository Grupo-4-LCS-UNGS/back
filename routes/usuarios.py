from flask import Blueprint, request, render_template, session, redirect, flash, url_for
from extensiones import db, bcrypt
from validaciones import *
from models.usuario import Usuario

usuarios = Blueprint('usuarios', __name__)

# endpoint de sign in
@usuarios.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('/signin.html')

    # capturamos los datos
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])
    rol = str(request.form['rol'])

    # validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        repetido = Usuario.encontrarPorNombre(nombre)  # Usamos el método del modelo

        if repetido is not None:
            flash('Usuario existente', 'message')
            return redirect(url_for('usuarios.signin'))
        else:
            encriptado = bcrypt.generate_password_hash(contrasena).decode('utf-8')
            nuevo_usuario = Usuario(nombre=nombre, contrasena=encriptado, rol=rol)  # Crear instancia de Usuario
            Usuario.agregar(nuevo_usuario)  # Agregar el nuevo usuario a la DB
            flash('Usuario dado de alta', 'success')
            return redirect(url_for('usuarios.inicio'))

    # Si las validaciones fallan, puedes manejar el error aquí
    flash('Datos inválidos', 'error')
    return redirect(url_for('usuarios.signin'))  # Redirigir de nuevo al formulario si hay errores

# endpoint de login
@usuarios.route('/login', methods=['GET', 'POST'])
def inicio():
    if request.method == 'GET':
        return render_template('login.html')
    
    # capturamos los datos 
    nombre = str(request.form['nombre'])
    contrasena = str(request.form['contrasena'])

    # validamos que cumplan con el formato
    if Valida.nombre(nombre) and Valida.contrasena(contrasena):
        personal = Usuario.encontrarPorNombre(nombre)  # Usamos el método del modelo

        if personal and bcrypt.check_password_hash(personal.contrasena, contrasena):  # Comparar contraseñas
            session['user_id'] = personal.id
            session['rol'] = personal.rol

            # redirigir según el rol
            rol = personal.rol
            ruta = None
            
            match rol:
                case 'Administrador':
                    ruta = 'administracion'
                case 'Operador':
                    ruta = 'operaciones'
                case 'Supervisor':
                    ruta = 'supervision'
                case 'Gerente':
                    ruta = 'gerente'
                case 'OpMantenimiento':
                    ruta = 'mantenimiento'
                case 'Cliente':
                    ruta = 'principal'

            flash('Login exitoso', 'success')

            return redirect(url_for(ruta))
        
        else:
            flash('Datos incorrectos', 'message')
            return redirect(url_for('usuarios.inicio'))

# endpoint de log out
@usuarios.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('rol', None)

    flash('Sesión cerrada con éxito', 'success')

    return redirect(url_for('index'))
