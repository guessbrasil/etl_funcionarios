import pandas as pd
import logging

def read_excel_file(filepath):
    try:
        df = pd.read_excel(filepath, sheet_name=0)
        logging.info(f"Arquivo lido com sucesso: {filepath}")
        return df
    except Exception as e:
        logging.error(f"Erro ao ler arquivo {filepath}: {e}")
        return None