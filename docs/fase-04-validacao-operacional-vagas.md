# Fase 4 - Validacao Operacional e Vagas

## 1. Objetivo

Permitir que o painel administrativo trate as inscricoes recebidas e confirme matriculas respeitando a capacidade da turma.

## 2. Por que este passo vem agora

Depois de receber a inscricao publica com protocolo, o fluxo precisa voltar para a operacao da escola, onde alguem analisa a solicitacao e decide o proximo estado.

## 3. Decisao tecnica

Foi implementado um primeiro recorte operacional com:

- atualizacao de status da inscricao;
- validacao de transicoes permitidas;
- bloqueio de confirmacao quando a turma atinge a capacidade;
- contagem inicial de confirmadas por turma;
- acao de status no painel admin;
- endpoint de API para atualizar status.

## 4. Regras atuais

- inscricoes podem evoluir entre `submitted`, `pending_validation`, `waitlisted`, `rejected` e `confirmed`;
- inscricoes confirmadas nao sao reabertas neste recorte;
- confirmacao so acontece se ainda houver vaga disponivel na turma;
- a ocupacao atual da turma considera apenas inscricoes `confirmed`.

## 5. Escopo deste recorte

- o admin consegue marcar uma inscricao em analise;
- o admin consegue confirmar, rejeitar ou mover para fila de espera;
- o painel mostra ocupacao e vagas restantes por turma;
- a API expoe a mudanca operacional de status.

## 6. O que ainda nao entrou

- reserva transacional real para disputa concorrente;
- cancelamento com devolucao de vaga;
- historico detalhado de auditoria por transicao;
- fila de espera automatica com promocao de inscricoes.

## 7. Beneficio de engenharia

Esse passo aproxima o produto do processo real da secretaria escolar, conectando o protocolo recebido pelo responsavel com a decisao operacional da escola.

## 8. Proximo passo natural

Depois deste modulo, o proximo bloco funcional e aprofundar consistencia de vagas, trilha de auditoria e anexos reais.
