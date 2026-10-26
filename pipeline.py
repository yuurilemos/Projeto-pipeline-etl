import logging
from extract import extract
from transform import transform
from validate import validate
from load import load

# 1. Configure o logging: logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
#    Para gravar também em arquivo, pesquise o parâmetro handlers com logging.FileHandler("pipeline.log")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

log = logging.getLogger(__name__)


def run():
    # 2. Extrair: chame extract() e registre com log.info(f"Extraídas {len(df)} linhas")
    df = extract()
    log.info(f"Extraídas {len(df)} linhas")
    # 3. Transformar: o mesmo, registrando as linhas que saíram
    df = transform(df)
    log.info(f"{len(df)} Linhas transformadas")
    # 4. Validar: registre "Validação OK" (se falhar, o raise já interrompe)
    df = validate(df)
    log.info("Validação OK")
    # 5. Carregar: registre que a tabela foi gravada
    load(df)
    log.info("Tabela gravada")


if __name__ == "__main__":
    run()