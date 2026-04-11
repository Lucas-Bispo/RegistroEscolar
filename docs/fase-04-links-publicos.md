# Fase 4 - Links Publicos

## 1. Objetivo

Adicionar o primeiro recorte funcional de publicacao da campanha de matricula.

## 2. Por que este passo vem agora

Depois de configurar escola, periodo, turma e formulario, o sistema precisa expor um acesso externo para o responsavel iniciar a matricula sem login.

## 3. Decisao tecnica

Foi implementado um modulo inicial de links publicos com:

- entidade de dominio para `public_link`;
- repositorio em memoria;
- servico de aplicacao;
- schemas Pydantic;
- rota de API;
- secao de criacao e listagem no painel admin;
- pagina publica resolvida por token.

## 4. Regras atuais

- link publico precisa apontar para escola, periodo e formulario existentes;
- o formulario precisa estar publicado;
- o formulario precisa pertencer a mesma escola e ao mesmo periodo do link;
- a expiracao precisa estar no futuro;
- o limite de envios precisa ser maior que zero;
- token e gerado de forma aleatoria no backend.

## 5. Escopo deste recorte

- o admin consegue gerar e listar links publicos;
- o responsavel consegue abrir uma pagina publica por token;
- o backend valida se o link existe, esta ativo e ainda nao expirou;
- a pagina publica renderiza os campos configurados do formulario publicado.

## 6. O que ainda nao entrou

- submissao da matricula;
- contagem real de envios por link;
- upload de documentos;
- validacao final com ocupacao de vagas;
- protocolo de inscricao.

## 7. Beneficio de engenharia

Esse passo fecha o primeiro fluxo visivel entre painel administrativo e area publica, mantendo o backend como fonte de verdade do token e do schema publicado.

## 8. Proximo passo natural

Depois deste modulo, o proximo bloco funcional e o registro da inscricao publica com validacoes de campos, selecao de turma e controle de vagas.
