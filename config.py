class Config:
    # Configuración para conectarse a la base de datos PostgreSQL
    HOST = 'localhost'
    PORT = 3306
    USER = 'root'
    PASSWORD = 'admin'
    DB = 'transportador'
    SECRET_KEY = 'admin'
    USER_DB = ''
    PASS_DB = ''
    URL_DB = 'localhost'
    NAME_DB = 'transportador'
    FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'