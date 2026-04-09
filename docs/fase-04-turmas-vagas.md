# Fase 4 - Turmas e Vagas

## 1. Objetivo

Adicionar ao painel administrativo o modulo de turmas e vagas.

## 2. Por que este modulo e central

No fluxo do produto, a matricula depende diretamente da existencia de:

- escola;
- periodo letivo;
- turma;
- capacidade maxima.

Ou seja, sem `classes`, ainda nao conseguimos chegar no formulario de matricula de forma coerente.

## 3. Regras iniciais implementadas

- cada turma pertence a uma escola;
- cada turma pertence a um periodo letivo;
- turma possui turno;
- turma possui capacidade maxima;
- capacidade deve ser maior que zero;
- nome da turma deve ser unico dentro da combinacao escola + periodo.

## 4. Observacao importante

Nesta fase, a capacidade ainda e apenas configurada e exibida.

O controle transacional de ocupacao de vagas durante a matricula sera aprofundado quando chegarmos nos modulos de:

- formulario publico;
- inscricao;
- confirmacao de matricula.

## 5. Beneficio arquitetural

Esse modulo reforca a ideia de composicao de dominios:

- `classes` depende do contexto de escolas;
- `classes` depende do contexto de periodos letivos;
- o painel admin passa a refletir melhor a sequencia real do produto.

## 6. Proximo passo natural

Depois de turmas e vagas, o proximo grande bloco funcional e o construtor de formulario dinamico.
