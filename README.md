# Pipeline ETL: Saldo de crédito com recursos livres (pessoas físicas)

Pipeline ETL em Python que extrai dados da API do Banco Central do Brasil, limpa e padroniza, valida e grava em um banco SQLite. Cada etapa é um módulo separado, a extração tenta de novo em caso de falha da API, a execução registra logs com contagem de linhas e a transformação e a validação são cobertas por testes automatizados com pytest.

## Fonte dos dados

- **Série:** SGS 20570, "Saldo da carteira de crédito com recursos livres - Pessoas físicas - Total"
- **Unidade:** R$ (milhões)
- **Periodicidade:** mensal, desde 01/03/2007 (sem data final: a série cresce todo mês)
- **Fonte:** Banco Central do Brasil, Departamento de Estatísticas (BCB-DSTAT)
- **Aviso do BCB:** série revisada integralmente em fevereiro de 2017
- **Endpoint:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.20570/dados?formato=json`

Os dados chegam como texto (`data` em dd/mm/aaaa e `valor` como string), o que torna a etapa de transformação necessária.

## Fluxo

```
API BCB  ->  extract  ->  transform  ->  validate  ->  load  ->  SQLite (pipeline.db)
```

| Etapa | Arquivo | O que faz |
|---|---|---|
| Extrair | `extract.py` | Chama a API com `requests` (timeout de 30 s, até 3 tentativas) e devolve um DataFrame |
| Transformar | `transform.py` | Padroniza nomes e converte tipos |
| Validar | `validate.py` | Confere se há linhas e se as colunas obrigatórias existem |
| Carregar | `load.py` | Grava a tabela `saldo_credito_pf` no SQLite via SQLAlchemy |
| Orquestrar | `pipeline.py` | Executa tudo em ordem e registra o log |
| Testes | `tests/` | Testes de `transform` e `validate` com pytest |

## Como instalar

```bash
git clone https://github.com/yuurilemos/Projeto-pipeline-etl.git
cd Projeto-pipeline-etl
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Como rodar

```bash
python pipeline.py
```

Ao final, o banco `pipeline.db` é criado na pasta do projeto com a tabela `saldo_credito_pf`. Para conferir:

```bash
sqlite3 pipeline.db "SELECT COUNT(*) FROM saldo_credito_pf;"
```

Cada etapa também pode ser executada isoladamente (por exemplo, `python extract.py` imprime o formato e as primeiras linhas dos dados brutos).

## Tolerância a falhas na extração

A API do Banco Central pode demorar ou falhar de forma passageira (o projeto já enfrentou um `ReadTimeout` real). Por isso a extração faz até 3 tentativas, com 5 segundos de espera entre elas:

- cada falha é registrada no log como aviso, com o número da tentativa;
- falhas de conexão, de tempo esgotado e respostas de erro do servidor geram nova tentativa;
- se as 3 tentativas falharem, o erro é repassado e o pipeline para antes de transformar ou gravar qualquer coisa, então o banco permanece como estava.

O número de tentativas e a espera ficam em constantes no topo do `extract.py` (`TENTATIVAS` e `ESPERA_SEGUNDOS`).

## Testes

```bash
pytest
```

São 8 testes, que não acessam a API nem o banco: usam DataFrames pequenos criados no próprio teste.

- **Transformação (`tests/test_transform.py`):** renomeia a coluna `valor` para `saldo_milhoes_brl`, converte `data` para datetime, converte o saldo para inteiro e não altera o DataFrame original.
- **Validação (`tests/test_validate.py`):** aceita um DataFrame válido e o devolve, e levanta `ValueError` para DataFrame vazio, para coluna ausente e com mensagem que cita a coluna que faltou.

Os testes foram conferidos quebrando o código de propósito (alterando o nome da coluna no `transform`): os testes correspondentes falharam, e voltaram a passar ao restaurar a linha. A configuração do pytest está em `pytest.ini`.

## Regras de transformação

1. Renomear a coluna `valor` para `saldo_milhoes_brl` (a unidade fica explícita no nome).
2. Converter `data` de texto (dd/mm/aaaa) para `datetime`.
3. Converter `saldo_milhoes_brl` de texto para inteiro.
4. Verificar nulos em todas as colunas (nenhum encontrado na série atual).

## Regras de validação

O pipeline para com `ValueError` e mensagem clara antes de gravar no banco se:

- o DataFrame estiver vazio;
- alguma coluna obrigatória (`data`, `saldo_milhoes_brl`) estiver ausente.

## Decisões de projeto

**Carga com `replace`.** A API devolve a série histórica completa a cada consulta, então a tabela é recriada a cada execução (`if_exists="replace"`). Isso mantém o banco sempre igual à fonte e evita duplicar linhas ao rodar de novo: a contagem permanece estável (234 linhas em agosto de 2026, mais uma por mês).

**Limitação.** O `replace` apaga e recria a tabela inteira, então não preserva histórico de cargas anteriores nem carrega só os dados novos.

**Retry simples.** A espera entre tentativas é fixa (5 s). Uma versão futura poderia aumentar a espera a cada tentativa (backoff exponencial).

## Exemplo de log

```
2026-10-22 17:23:42,701 INFO Extraídas 234 linhas
2026-10-22 17:23:42,710 INFO Nulos encontrados: 0
2026-10-22 17:23:42,710 INFO Linhas 234 transformadas
2026-10-22 17:23:42,710 INFO Validação OK
2026-10-22 17:23:42,736 INFO Tabela gravada
```


## Próximos passos

- Testes automatizados para o retry da extração.
- Carga incremental com `append`, gravando só as datas novas.
- Gravar o log também em arquivo.

## Tecnologias

Python, pandas, requests, SQLAlchemy, SQLite, pytest.
