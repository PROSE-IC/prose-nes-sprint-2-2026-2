# PROSE NES 2026/2 - Sprint 2

Dashboard por equipe para as devolutivas do Survey Alunos, com historico das Sprints 0 e 1 e resultados da Sprint 2.

## Equipes disponibilizadas

| Equipe | Projeto | Supervisor(a) | Periodo | Respostas Sprint 2 |
| --- | --- | --- | --- | --- |
| T1 | Biblioteca do NDH | Marcio | Vespertino | 6/6 (100,0%) |
| T7 | Notifica Saude | Turine | Noturno | 1/6 (16,7%) |

Publicacao inicial em 20/10/2026, do T1. T7 acrescentado em 27/10/2026, com seu relatorio PDF. Outras equipes poderao ser acrescentadas posteriormente, preservando a mesma estrutura.

No T1, a contagem representa seis envios classificados para a equipe, sendo tres nominais e tres com pseudonimo. Pseudonimos nao permitem confirmar a identidade individual de cada respondente. O historico do T1 foi preservado do repositorio da Sprint 1, sem recalcular as notas anteriores.

O T7 tem um envio identificado por pseudonimo de equipe. Seus relatos das Sprints 0 e 1 tambem foram preservados do repositorio anterior, sem recalculo. As contagens representam envios classificados, nao uma verificacao independente de identidades.

## Estrutura

- `common/dashboard_app.py`: motor compartilhado dos dashboards.
- `teams/t1/app.py`: entrada independente do T1 no Streamlit.
- `teams/t1/data/relatos/`: relatos agregados das Sprints 0, 1 e 2.
- `teams/t7/app.py`: entrada independente do T7, com relatos agregados das Sprints 0, 1 e 2.
- `pdfs/relatorio_T7_sprint_2.pdf`: devolutiva do T7 no modelo aprovado de cinco paginas.
- `common/pdf_report.py`, `assets/` e `scripts/export_team_pdf.py`: modelo e exportador do PDF.
- `docs/metodologia-dashboard.md`: criterios de calculo e interpretacao.
- `tests/test_dashboard.py`: verificacoes de leitura, filtros e comparacao contextual.

Para acrescentar outra equipe, manter uma entrada `teams/tX/app.py` e seus relatos agregados em `teams/tX/data/relatos/`.

## Streamlit Community Cloud

Selecionar este repositorio, branch `main`, e a entrada:

```text
teams/t1/app.py
```

Para o T7, usar `teams/t7/app.py`.

Para executar localmente:

```powershell
pip install -r requirements.txt
streamlit run teams/t1/app.py
```

## Calculo e comparacao

O processamento usa o mesmo schema das publicacoes anteriores: normalizacao pelas escalas reais, inversao dos itens negativos e nota geral ponderada pelos cinco blocos de perguntas. A Media SPACE filtrada e uma agregacao distinta da Nota do Survey. Activity nao e calculada pelo survey nesta versao.

Respostas vazias e "Prefiro nao responder" permanecem ausentes, sem imputacao de zero. Itens parcialmente respondidos indicam a base valida quando aparecem entre os pontos fortes ou de atencao. Na Sprint 2 do T1, o item condicional de discussao da solucao tem duas respostas validas, e o item sobre fatores externos tem cinco.

No T7, o item condicional de discussao da solucao nao tem resposta valida. Ele nao recebeu zero e foi excluido dos pontos fortes e de atencao.

A comparacao contextual exige pelo menos duas equipes na mesma sprint. A referencia atual inclui T1 e T7 e usa a media simples dos escores por equipe na sprint, incluindo a propria, sem ponderar pelo numero de envios e sem ranking. Nao representa todas as dez equipes do semestre.

## Privacidade e escopo

Este repositorio contem codigo, relatos agregados e o PDF de devolutiva autorizado. A planilha de respostas, nomes de estudantes, respostas abertas, auditorias de identificacao e JSONs locais de processamento nao sao publicados.

Esta entrega inclui os dashboards de T1 e T7 e o PDF da Sprint 2 do T7. Nao inclui novo deployment no Streamlit Cloud. Os dados ja publicados do T1 nao foram recalculados nesta atualizacao.

## Testes

```powershell
python -m unittest discover -s tests -v
```
