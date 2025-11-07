import logging
from urllib.parse import quote_plus
from sqlalchemy import create_engine
import pandas as pd

def load_to_database(df, engine, db_config):
    try:
        df = df.replace({pd.NA: None, '': None, 'nan': None})
        df = df.where(pd.notnull(df), None)
        df = df.drop_duplicates(subset=['CPF'])

        with engine.begin() as conn:  
            existing_cpfs = pd.read_sql(f"SELECT CPF FROM {db_config['tabela_destino']}", conn)
            existing_cpfs_list = existing_cpfs['CPF'].tolist()
            df_filtered = df[~df['CPF'].isin(existing_cpfs_list)]

            if df_filtered.empty:
                logging.info("Nenhum novo registro para inserir.")
                return True

            df_filtered.to_sql(db_config['tabela_destino'], con=conn, if_exists='append', index=False)

        logging.info(f"{len(df_filtered)} novos registros inseridos no banco de dados.")
        return True

    except Exception as e:
        logging.error(f"Erro ao inserir dados no banco: {e}")
        return False
