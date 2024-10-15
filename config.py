class Config:
    # Configuración para conectarse a la base de datos PostgreSQL
    HOST = 'localhost'
    PORT = 5432
    USER = 'postgres'
    PASSWORD = 'postgres'
    DB = 'transportador'
    SECRET_KEY = 'admin'
    FULL_URL_DB = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'