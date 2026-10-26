import requests
import time 
import logging
import pandas as pd

URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.20570/dados?formato=json"
TENTATIVAS = 3 
ESPERA_SEGUNDOS = 5

log = logging.getLogger(__name__)


def extract():
    for tentativa in range(1, TENTATIVAS + 1):
        try:
            resposta = requests.get(URL, timeout = 30)
            resposta.raise_for_status()
            break
        except requests.exceptions.RequestException as erro:
            log.warning(f"Tentaiva {tentativa}/{TENTATIVAS} falhou: {erro}")
            if tentativa == TENTATIVAS:
                raise 
            else:
                time.sleep(ESPERA_SEGUNDOS)


    dados = resposta.json()
    df = pd.DataFrame(dados)
    return df 