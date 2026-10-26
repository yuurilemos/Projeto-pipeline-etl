import pandas as pd
import pytest
from validate import validate


def df_valido():
    # DataFrame de 2 ou 3 linhas já transformado, com as colunas
    # "data" (datas) e "saldo_milhoes_brl" (números inteiros)
    dados = {
        "data": pd.to_datetime(["20/10/2014", "03/05/2018", "20/05/2008"], format="%d/%m/%Y"),
        "saldo_milhoes_brl" : [220000, 23000, 650000],
    }
    return pd.DataFrame(dados)


def test_df_valido_passa_e_e_devolvido():
    df = df_valido()   #  criar com df_valido()
    resultado = validate(df)   #  rodando validate(df) 
    assert len(resultado) == len(df)   #  o resultado tem o mesmo número de linhas que df (use len)


def test_df_vazio_levanta_erro():
    with pytest.raises(ValueError):
        validate(pd.DataFrame())       # chamando validate(pd.DataFrame())


def test_coluna_ausente_levanta_erro():
    df = df_valido().drop(columns = ["saldo_milhoes_brl"])    # df_valido() sem a coluna "saldo_milhoes_brl" 
    with pytest.raises(ValueError):
        validate(df)       # chamando alidate(df)


def test_mensagem_cita_a_coluna_que_faltou():
    df = df_valido().drop(columns = ["saldo_milhoes_brl"])     # o mesmo df sem a coluna
    with pytest.raises(ValueError, match="saldo_milhoes_brl"):
        validate(df)       # chamando validate(df)