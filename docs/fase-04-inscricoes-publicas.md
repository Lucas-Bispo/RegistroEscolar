# Fase 4 - Inscricoes Publicas

## 1. Objetivo

Transformar a pagina publica da campanha em um fluxo capaz de receber uma inscricao real.

## 2. Por que este passo vem agora

Depois de publicar o formulario e expor o link, o proximo passo natural e permitir que o responsavel envie os dados preenchidos e receba um protocolo.

## 3. Decisao tecnica

Foi implementado um modulo inicial de inscricoes com:

- entidade de dominio para `enrollment`;
- repositorio em memoria;
- servico de aplicacao;
- schema Pydantic;
- rota de API para submissao publica;
- POST da pagina `/matricula/{token}`;
- pagina de sucesso com protocolo;
- listagem inicial das inscricoes no painel admin.

## 4. Regras atuais

- a inscricao precisa usar um link publico ativo e nao expirado;
- a turma selecionada precisa pertencer a mesma escola e ao mesmo periodo do link;
- a turma precisa estar ativa;
- os campos obrigatorios do formulario precisam ser preenchidos;
- campos `select` precisam respeitar as opcoes publicadas;
- links respeitam o limite configurado de envios;
- cada inscricao gera um protocolo unico amigavel.

## 5. Escopo deste recorte

- o responsavel consegue escolher uma turma e enviar o formulario;
- o backend valida os dados principais antes de persistir;
- a inscricao fica registrada em memoria;
- a tela de sucesso mostra o protocolo e um resumo das respostas;
- o painel admin ja consegue visualizar as inscricoes recebidas.

## 6. O que ainda nao entrou

- upload real de arquivos;
- workflow de validacao operacional;
- confirmacao final de matricula;
- ocupacao transacional de vagas;
- consulta publica posterior por protocolo.

## 7. Beneficio de engenharia

Esse passo fecha o primeiro fluxo ponta a ponta do produto: configuracao interna, publicacao externa, submissao publica e retorno rastreavel ao usuario.

## 8. Proximo passo natural

Depois deste modulo, o proximo bloco funcional e a validacao operacional da inscricao com controle de vagas por turma e evolucao de status.
