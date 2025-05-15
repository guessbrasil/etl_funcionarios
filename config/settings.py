import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#DATA_DIR = os.path.join(BASE_DIR, 'data')
ENTRADA_DIR = os.path.join(BASE_DIR, 'processar')
LIDOS_DIR = os.path.join(BASE_DIR, 'lidos')
LOG_DIR = os.path.join(BASE_DIR, 'logs')

DB_CONFIG = {
    'usuario': os.getenv('DB_USUARIO'),
    'senha': os.getenv('DB_SENHA'),
    'servidor': os.getenv('DB_SERVIDOR'),
    'banco': os.getenv('DB_BANCO'),
    'tabela_destino': os.getenv('TABELA_DESTINO'),
    'driver': os.getenv('DB_DRIVER')  
}

LOCKFILE = os.path.join(BASE_DIR, 'etl_funcionarios.lock')
LOGFILE = os.path.join(LOG_DIR, 'etl_funcionarios.log')
