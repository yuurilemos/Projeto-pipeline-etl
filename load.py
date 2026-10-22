from sqlalchemy import create_engine
import pandas as pd
from extract import extract
from transform import transform
from validate import validate

DB_URL = "sqlite:///pipeline.db"
TABELA = "saldo_credito_pf"


def load(df):
    # Criando a conexao 
    engine = create_engine(DB_URL)
    # Gravando df na tabela
    df.to_sql(TABELA, engine, if_exists = "replace", index = False)

    return engine 


if __name__ == "__main__":
    df = validate(transform(extract()))
    engine = load(df)
    # Conferindo resultado
    print(pd.read_sql(f"SELECT COUNT(*) AS total FROM {TABELA}", engine))
    