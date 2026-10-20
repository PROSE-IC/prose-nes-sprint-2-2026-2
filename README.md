# PROSE NES 2026/2 - Sprint 2

Dashboard por equipe para as devolutivas do Survey Alunos, com historico das Sprints 0 e 1 e resultados da Sprint 2.

## Equipes disponibilizadas

| Equipe | Projeto | Supervisor(a) | Periodo | Respostas Sprint 2 |
| --- | --- | --- | --- | --- |
| T1 | Biblioteca do NDH | Marcio | Vespertino | 6/6 (100,0%) |

Publicacao inicial em 20/10/2026, somente do T1. Outras equipes poderao ser acrescentadas posteriormente, preservando a mesma estrutura.

A contagem representa seis envios classificados para a equipe, sendo tres nominais e tres com pseudonimo. Pseudonimos nao permitem confirmar a identidade individual de cada respondente. O historico do T1 foi preservado do repositorio da Sprint 1, sem recalcular as notas anteriores.

## Estrutura

- `common/dashboard_app.py`: motor compartilhado dos dashboards.
- `teams/t1/app.py`: entrada independente do T1 no Streamlit.
- `teams/t1/data/relatos/`: relatos agregados das Sprints 0, 1 e 2.
- `docs/metodologia-dashboard.md`: criterios de calculo e interpretacao.
- `tests/test_dashboard.py`: verificacoes de leitura, filtros e comparacao contextual.

Para acrescentar outra equipe, manter uma entrada `teams/tX/app.py` e seus relatos agregados em `teams/tX/data/relatos/`.

## Streamlit Community Cloud

Selecionar este repositorio, branch `main`, e a entrada:

```text
teams/t1/app.py
```

Para executar localmente:

```powershell
pip install -r requirements.txt
streamlit run teams/t1/app.py
```

## Calculo e comparacao

O processamento usa o mesmo schema das publicacoes anteriores: normalizacao pelas escalas reais, inversao dos itens negativos e nota geral ponderada pelos cinco blocos de perguntas. A Media SPACE filtrada e uma agregacao distinta da Nota do Survey. Activity nao e calculada pelo survey nesta versao.

Respostas vazias e "Prefiro nao responder" permanecem ausentes, sem imputacao de zero. Itens parcialmente respondidos indicam a base valida quando aparecem entre os pontos fortes ou de atencao. Na Sprint 2 do T1, o item condicional de discussao da solucao tem duas respostas validas, e o item sobre fatores externos tem cinco.

A comparacao contextual exige pelo menos duas equipes na mesma sprint. Enquanto apenas o T1 estiver publicado, o painel informa essa limitacao e nao apresenta uma comparacao da equipe consigo mesma. Com outras equipes, a referencia sera a media simples dos escores por equipe na sprint, incluindo a propria, sem ponderar pelo numero de envios e sem ranking.

## Privacidade e escopo

Este repositorio contem apenas codigo e relatos agregados necessarios ao dashboard. A planilha de respostas, nomes de estudantes, respostas abertas, auditorias de identificacao e JSONs locais de processamento nao sao publicados.

Esta entrega inclui somente o dashboard do T1. Nao inclui relatorio PDF ou novo deployment no Streamlit Cloud.

## Testes

```powershell
python -m unittest discover -s tests -v
```
