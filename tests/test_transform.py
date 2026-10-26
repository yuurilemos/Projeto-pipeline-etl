import pandas as pd
from transform import transform


def df_bruto():
    # Montar um DataFrame igual ao que aparece na API
    dados = {
        "data" : ["07/10/2015", "20/03/2007", "03/09/2008"],
        "valor" : ["245676", "1245670", "24500"],
    }
    return pd.DataFrame(dados)

def test_renomeia_coluna_valor():
    # chamando transform(df_bruto()) e afirmando que "saldo_milhoes_brl" está em df.columns
    df = transform(df_bruto())
    assert "saldo_milhoes_brl" in df.columns 
    assert "valor" not in df.columns

def test_converte_data_para_datetime():
    # dica de função: pd.api.types.is_datetime64_any_dtype(df["data"])
    df = transform(df_bruto())
    assert pd.api.types.is_datetime64_any_dtype(df["data"])

def test_converte_saldo_para_inteiro():
    # dica de função: pd.api.types.is_integer_dtype(df["saldo_milhoes_brl"])
    df = transform(df_bruto())
    assert pd.api.types.is_integer_dtype(df["saldo_milhoes_brl"])

def test_nao_altera_o_df_original():
    # guarde o df antes, rode transform e afirme que o original ainda tem a coluna "valor"
    original = df_bruto()
    transform(original)
    assert "valor" in original.columns