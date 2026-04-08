# ADR 0001 - Escolha de monolito modular para o backend

## Status

Aceito

## Contexto

O projeto `RegistroEscolar` e uma plataforma SaaS de matricula online com:

- multi-tenant por escola;
- formularios dinamicos;
- links publicos;
- controle de vagas com consistencia forte;
- necessidade de desenvolvimento local em WSL Ubuntu;
- deploy futuro em servidor Linux.

Precisamos de uma arquitetura que:

- seja simples o bastante para evoluir com seguranca;
- suporte crescimento de dominio;
- facilite testes e manutencao;
- nao imponha complexidade operacional precoce.

## Decisao

Adotar um **monolito modular** no backend Python.

O sistema sera organizado por modulos de dominio e camadas internas, mantendo separacao entre:

- API;
- services;
- domain;
- infrastructure;
- schemas;
- core.

## Consequencias positivas

- menor complexidade operacional inicial;
- maior produtividade no comeco do projeto;
- melhor experiencia para aprendizado e onboarding;
- deploy mais simples;
- debug mais facil;
- ainda permite crescimento com boa modularidade.

## Trade-offs

- requer disciplina arquitetural para nao virar monolito acoplado;
- pode exigir extracao futura de componentes se o produto crescer muito;
- demanda cuidado para manter fronteiras de modulo bem definidas.

## Alternativas consideradas

### Microsservicos

Rejeitado neste momento por aumentar:

- custo de infraestrutura;
- complexidade de observabilidade;
- dificuldade de integracao;
- sobrecarga operacional.

### Estrutura flat minimalista

Rejeitada porque o dominio do produto nao e trivial e exige maior organizacao para preservar coesao e testabilidade.
