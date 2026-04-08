# Fase 4 - Interface Web Inicial

## 1. Objetivo

Adicionar uma interface grafica inicial sem abandonar a arquitetura orientada a API.

## 2. Decisao tecnica

Foi escolhida uma interface server-side simples com `Jinja2` integrada ao `FastAPI`.

### Por que essa escolha faz sentido agora

- entrega valor visual rapidamente;
- reduz complexidade inicial em comparacao com um frontend separado;
- preserva a API como nucleo do sistema;
- facilita aprendizado incremental.

## 3. Trade-off

Essa nao e necessariamente a arquitetura final do painel administrativo.

No futuro, ainda podemos:

- evoluir essa interface;
- extrair um frontend separado;
- manter a API como backend oficial.

## 4. Funcionalidades visuais atuais

- dashboard inicial em `/`;
- exibicao das escolas cadastradas;
- formulario para cadastro de nova escola;
- links rapidos para API e documentacao.

## 5. Beneficio de engenharia

Essa abordagem preserva:

- `SRP`: API continua com responsabilidade de contrato HTTP JSON;
- `baixo acoplamento`: a camada HTML consome os mesmos servicos;
- `reuso`: a regra de negocio nao foi duplicada na interface.
