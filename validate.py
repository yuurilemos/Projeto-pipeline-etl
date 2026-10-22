import pandas as pd
from extract import extract
from transform import transform

COLUNAS_OBRIGATORIAS = ["data", "saldo_milhoes_brl"]


def validate(df):
    # Conferindo se o df esta vazio
    if df.empty: 
        raise ValueError("O DataFrame está vazio: nenhuma lista recebida da API")
    # Descobrindo se faltam colunas obrigatorias
    faltando = []
    for coluna in COLUNAS_OBRIGATORIAS:
        if coluna not in df.columns:
            faltando.append(coluna)

    if faltando:
        raise ValueError(f"Colunas ausentes: {faltando}")
    
    # return
    return df

if __name__ == "__main__":
    df = validate(transform(extract()))
    print("Validação OK:", df.shape)