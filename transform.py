import pandas as pd
import logging
from extract import extract

log = logging.getLogger(__name__)

def transform(df):
    # Copiando df para nao alterar o original
    df = df.copy()
    # Renomeando as colunas
    df = df.rename(columns = {"data": "data", "valor" : "saldo_milhoes_brl"})
    # Convertendo a coluna de data
    df["data"] = pd.to_datetime(df["data"], format = "%d/%m/%Y")
    # Convertendo o saldo para numero
    df["saldo_milhoes_brl"] = pd.to_numeric(df["saldo_milhoes_brl"])
    # Verificando os nulos
    log.info(f"Nulos encontrados: {df.isna().sum().sum()}")
    
    # return df 

    return df


if __name__ == "__main__":
    df = transform(extract())
    # print df.dtypes e df.head()
    print(df.dtypes)
    print(df.head())