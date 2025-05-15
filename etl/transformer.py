import pandas as pd
import logging

def transform_dataframe(df):
    try:
        df_formatado = pd.DataFrame({
            'Nome_Empresa_Filial': df['Razão Social Empresa/Filial'],  
            'CNPJ_Empresa_Filial': df['CNPJ Empresa/Filial'], 
            'Status': df['Status do Funcionário'], 
            'Matricula': df['Matricula'],
            'Nome': df['Nome da Pessoa'],
            'CPF': df['Numero do CPF'],
            'RG': df['Numero do RG'],
            'Sexo': df['Sexo'],
            'Cep': df['Cep'],
            'Endereco': df['Endereço'],
            'Numero': df['Numero do Endereço'].fillna(0).astype(int).astype(str),
            'Complemento': df['Complemento do Endereço'],
            'Cidade': df.get('Cidade do Endereço'), 
            'Estado': df['Estado do Endereço'],
            'Pais': df['País'],
            'Email': df['Email Pessoal']
        }).astype(str)

        #df_formatado = df_formatado.fillna('NULL').replace('', 'NULL')
        df_formatado = df_formatado.astype(str)
        df_formatado = df_formatado.replace(['nan', 'None', ''], None)

        if df_formatado['CPF'].isnull().any():
            logging.warning("DataFrame contém CPF nulo. Abortando transformação.")
            return None

        return df_formatado
    except Exception as e:
        logging.error(f"Erro na transformação dos dados: {e}")
        return None
