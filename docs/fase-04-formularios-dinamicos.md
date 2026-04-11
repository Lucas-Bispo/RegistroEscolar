# Fase 4 - Formularios Dinamicos

## 1. Objetivo

Iniciar o construtor de formularios dinamicos no painel administrativo.

## 2. Por que este passo vem agora

Depois de escola, periodo letivo e turma, o proximo bloco funcional natural e definir o que o responsavel precisara preencher no fluxo publico de matricula.

Sem esse passo, ainda nao conseguimos preparar:

- schema publicado da campanha;
- validacoes configuraveis por campo;
- base para o futuro link publico.

## 3. Decisao tecnica

Foi implementado um primeiro modulo de formularios com:

- entidade de dominio para formulario;
- entidade de dominio para campo configuravel;
- contrato de repositorio;
- repositorio em memoria;
- servico de aplicacao;
- schemas Pydantic;
- rota de API;
- secao inicial no painel admin.

## 4. Escopo deste primeiro recorte

- formulario vinculado a escola e periodo letivo;
- nome e descricao do formulario;
- lista ordenada de campos;
- tipos iniciais de campo:
  - `text`
  - `date`
  - `email`
  - `phone`
  - `select`
  - `upload`
- estado inicial de `rascunho` ou `publicado`.

## 5. Regras atuais

- formulario deve pertencer a uma escola existente;
- formulario deve pertencer a um periodo letivo existente;
- nome deve ser unico dentro da combinacao escola + periodo;
- formulario deve ter pelo menos um campo;
- ordem dos campos deve ser unica;
- apenas `select` pode receber opcoes;
- `select` precisa ter ao menos uma opcao.

## 6. Trade-off atual

No painel administrativo, os campos sao informados inicialmente em JSON.

Isso nao representa a experiencia final do produto, mas permite validar rapidamente:

- modelagem do schema;
- regras do backend;
- persistencia do formulario;
- integracao entre painel e API.

## 7. Beneficio de engenharia

Esse recorte prepara o caminho para os proximos passos sem acoplar cedo demais a interface final:

- publicacao versionada;
- link publico de matricula;
- renderizacao dinamica do formulario;
- validacao backend da inscricao.

## 8. Proximo passo natural

Depois deste modulo, o proximo bloco funcional e a publicacao do link publico associado a escola, periodo e formulario.
