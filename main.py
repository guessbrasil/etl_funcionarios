# main.py

import os
import sys
import shutil
import logging
from config import settings
from etl.reader import read_excel_file
from etl.transformer import transform_dataframe
from etl.loader import load_to_database

os.makedirs(settings.LOG_DIR, exist_ok=True)
os.makedirs(settings.ENTRADA_DIR, exist_ok=True)
os.makedirs(settings.LIDOS_DIR, exist_ok=True)

logging.basicConfig(
    filename=settings.LOGFILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def process_file(filepath):
    logging.info(f"Iniciando processamento do arquivo: {filepath}")
    df_raw = read_excel_file(filepath)
    if df_raw is None:
        return

    df_transformado = transform_dataframe(df_raw)
    if df_transformado is None:
        return

    sucesso = load_to_database(df_transformado, settings.DB_CONFIG)
    if sucesso:
        destino = os.path.join(settings.LIDOS_DIR, os.path.basename(filepath))
        shutil.move(filepath, destino)
        logging.info(f"Arquivo movido para lidos: {destino}")
