# Task 04 — Especificar fluxo completo: configurar formulário → gerar link público → matrícula

## Objetivo
Detalhar o fluxo de ponta a ponta com regras de negócio, validações e estados de matrícula.

## Escopo
- Fluxo administrativo de configuração.
- Geração e gestão de link público por escola/período.
- Fluxo público sem login.
- Tratamento de concorrência de vagas em tempo real.

## Fluxo detalhado
### 1) Configuração administrativa
1. Admin seleciona escola e período letivo.
2. Admin cria/edita turmas (nome, turno, capacidade máxima).
3. Admin cria versão do formulário dinâmico.
4. Admin adiciona campos, regras, máscaras e ordem de exibição.
5. Admin publica versão do formulário.

### 2) Geração de link público
1. Sistema cria `public_link` com token aleatório seguro e escopo (escola + período + versão).
2. Define validade, limite de requisições e status ativo/inativo.
3. Link é disponibilizado para comunicação externa.

### 3) Matrícula pelo responsável (sem login)
1. Responsável abre link público.
2. Front busca schema da versão publicada.
3. Formulário é renderizado dinamicamente.
4. Responsável preenche dados e seleciona turma.
5. Backend valida dados + disponibilidade da turma.
6. Uploads são enviados por URL pré-assinada e vinculados à inscrição.
7. Transação final confirma matrícula apenas se houver vaga.
8. Sistema retorna protocolo de inscrição.

## Estados sugeridos de matrícula
- `draft`
- `submitted`
- `pending_validation`
- `confirmed`
- `rejected`
- `waitlisted`
- `cancelled`

## Regras críticas
- Turma lotada deve bloquear confirmação imediatamente.
- Campo obrigatório e validações devem ser executados em backend (não só no frontend).
- Matrícula deve ficar vinculada à versão exata do formulário publicada.

## Critérios de aceite
- Fluxo BPMN (ou sequência) documentado.
- Regras de transição de status definidas.
- Casos de erro mapeados (link expirado, turma lotada, upload inválido).

## Dependências
- Task 01 e Task 02.
