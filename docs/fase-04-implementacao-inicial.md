# Fase 4 - Implementacao Inicial

## 1. Objetivo da fase

Iniciar a implementacao do backend sem tentar construir todo o produto de uma vez.

Nesta etapa, seguimos um principio importante de engenharia: **incrementalismo**.

Em vez de implementar matriculas, uploads, autenticacao e banco ao mesmo tempo, comecamos com um primeiro **recorte vertical** simples e didatico.

## 2. Recorte escolhido

O primeiro modulo funcional implementado foi o modulo de `schools`.

### Por que comecar por `schools`

- e um dominio central do produto;
- tem regra de negocio simples;
- exercita a arquitetura em camadas;
- permite validar organizacao de `domain`, `services`, `schemas`, `infrastructure` e `api`;
- evita complexidade prematura com banco de dados.

## 3. Estrategia tecnica

Foi usada uma implementacao **em memoria** como repositorio inicial.

### Motivo da escolha

Essa decisao segue `KISS`:

- validamos design e fluxo da aplicacao antes de integrar PostgreSQL;
- reduzimos o custo cognitivo para o inicio do projeto;
- deixamos clara a separacao entre regra de negocio e persistencia.

No futuro, o repositorio em memoria sera substituido por uma implementacao baseada em banco sem precisar reescrever as rotas ou os servicos.

## 4. Componentes adicionados

- `domain/schools/entities.py`
- `domain/schools/repositories.py`
- `infrastructure/repositories/in_memory_school_repository.py`
- `services/schools.py`
- `schemas/schools.py`
- `api/routers/schools.py`

## 5. O que o modulo faz hoje

- listar escolas;
- buscar escola por identificador;
- criar escola em memoria;
- validar duplicidade de nome normalizado.

## 6. O que ele ainda nao faz

- persistencia real em banco;
- autenticacao;
- isolamento multi-tenant completo;
- edicao e remocao;
- paginacao;
- auditoria persistente.

## 7. Beneficio arquitetural

Essa implementacao mostra, na pratica, como a arquitetura definida na Fase 2 funciona:

- a API recebe a requisicao;
- os `schemas` validam o contrato externo;
- o `service` aplica regra de negocio;
- o `repository` abstrai a persistencia;
- o dominio concentra a modelagem principal.

## 8. Como acompanhar em localhost

Quando o ambiente Python estiver ativo no WSL Ubuntu e as dependencias estiverem instaladas, voce podera acessar:

- `http://localhost:8000/`
- `http://localhost:8000/docs`
- `http://localhost:8000/api/v1/health`
- `http://localhost:8000/api/v1/schools`

## 9. Proximos passos naturais

Depois deste recorte inicial, a evolucao mais natural sera:

- integrar persistencia real;
- adicionar modulos de periodos letivos e turmas;
- introduzir tratamento de erros padronizado;
- ampliar a documentacao da API.
