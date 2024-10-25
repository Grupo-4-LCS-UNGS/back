from dotenv import load_dotenv
import os



if not os.getenv('ENV'):
    os.environ['ENV'] = 'development'
    
if os.getenv('ENV') == 'development' or os.getenv('ENV') == 'devops':
    env_file = f'.env.{os.getenv("ENV")}'
    load_dotenv(env_file)




class Config:
    # Configuración para conectarse a la base de datos PostgreSQL
    HOST = os.getenv('DB_HOST')
    PORT = int(os.getenv('DB_PORT'))
    USER = os.getenv('DB_USER')
    PASSWORD = os.getenv('DB_PASSWORD')
    DB = os.getenv('DB_NAME')
    SECRET_KEY = os.getenv('SECRET_KEY')
    FULL_URL_DB = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'