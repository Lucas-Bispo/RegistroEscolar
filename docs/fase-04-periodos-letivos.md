# Fase 4 - Periodos Letivos

## 1. Objetivo

Adicionar ao painel administrativo o primeiro modulo de configuracao operacional depois do login: periodos letivos.

## 2. Por que este passo vem agora

No fluxo do produto, o admin nao deveria sair criando formulario ou link publico sem antes definir o contexto da campanha.

Esse contexto e dado por:

- escola;
- periodo letivo;
- turmas;
- formulario publicado.

Por isso, `academic_terms` vem antes de `classes` e antes do construtor do formulario.

## 3. Decisao tecnica

Foi implementado um modulo inicial de periodos letivos com:

- entidade de dominio;
- contrato de repositorio;
- repositorio em memoria;
- servico de aplicacao;
- schemas Pydantic;
- rota de API;
- formulario no painel admin.

## 4. Regras atuais

- nome do periodo deve ser unico;
- data de inicio nao pode ser maior que a data de fim;
- periodo pode estar ativo ou inativo.

## 5. Beneficio de engenharia

Esse modulo reforca a arquitetura em camadas:

- `domain` modela o conceito;
- `services` concentram as regras;
- `infrastructure` cuida da persistencia atual;
- `api` expõe JSON;
- `web` oferece a manipulacao visual no painel admin.

## 6. Proximo passo natural

Depois de periodos letivos, o modulo mais importante e `classes`, porque ele traz:

- turmas;
- vagas;
- turno;
- base para selecao no formulario de matricula.
