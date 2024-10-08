from flask_sqlalchemy import SQLAlchemy

db2 = SQLAlchemy()

# ESTO VA EN EL main.py
#Configuración de la bd
# USER_DB = ''
# PASS_DB = ''
# URL_DB = 'localhost'
# NAME_DB = 'transportador'
# FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'
#
# app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db2.init_app(app)