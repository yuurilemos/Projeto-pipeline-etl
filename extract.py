import requests
import pandas as pd

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.20570/dados?formato=json"


def extract():
    # Chamando a API e guardando na variavel : resposta 
    resposta = requests.get(URL, timeout = 30)
    # Verificando se deu erro 
    resposta.raise_for_status()
    # Convetendo a resposta em lista de dicionarios e guardando em dados
    dados = resposta.json()
    # Transformando em DataFrame e guardando em df 
    df = pd.DataFrame(dados)
    # Devolvendo df
    return df 

if __name__ == "__main__":
    df = extract()
    # print df.shape
    print(df.shape)
    # print df.head()
    print(df.head())