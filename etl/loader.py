import logging
from urllib.parse import quote_plus
from sqlalchemy import create_engine
import pandas as pd

def load_to_database(df, db_config):
    try:

        df = df.replace({pd.NA: None, '': None, 'nan': None})
        df = df.where(pd.notnull(df), None)  
   
        df = df.drop_duplicates(subset=['CPF'])

        connection_string = (
            f"DRIVER={db_config['driver']};"
            f"SERVER={db_config['servidor']};"
            f"DATABASE={db_config['banco']};"
            f"UID={db_config['usuario']};"
            f"PWD={db_config['senha']}"
        )
        conn_str = f"mssql+pyodbc:///?odbc_connect={quote_plus(connection_string)}"
        engine = create_engine(conn_str)

        with engine.connect() as conn:
            existing_cpfs = pd.read_sql(
                f"SELECT CPF FROM {db_config['tabela_destino']}", conn
            )['CPF'].tolist()

        df_filtered = df[~df['CPF'].isin(existing_cpfs)]

        if df_filtered.empty:
            logging.info("Nenhum novo registro para inserir.")
            return True

        df_filtered.to_sql(db_config['tabela_destino'], con=engine, if_exists='append', index=False)

        logging.info(f"{len(df_filtered)} novos registros inseridos no banco de dados.")
        return True

    except Exception as e:
        logging.error(f"Erro ao inserir dados no banco: {e}")
        return False
