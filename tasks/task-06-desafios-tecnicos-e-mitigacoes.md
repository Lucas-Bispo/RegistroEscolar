# Task 06 — Mapear desafios técnicos e estratégias de mitigação

## Objetivo
Antecipar riscos arquiteturais e operacionais do projeto e definir soluções práticas.

## Escopo
- Concorrência em vagas.
- Evolução de formulários dinâmicos sem quebrar histórico.
- Escalabilidade multi-escola.
- Conformidade e proteção de dados.

## Desafios e soluções
### 1) Corrida por vagas em horários de pico
- **Risco:** duas inscrições simultâneas ocuparem a mesma última vaga.
- **Mitigação:** lock transacional em turma (`FOR UPDATE`) + validação final no commit.

### 2) Mudança de formulário durante período de matrícula
- **Risco:** respostas antigas ficarem incompatíveis.
- **Mitigação:** versionamento imutável; nova edição gera nova versão sem alterar inscrições passadas.

### 3) Uploads maliciosos ou inválidos
- **Risco:** segurança e armazenamento contaminado.
- **Mitigação:** validação dupla (cliente + servidor), antivírus assíncrono, quarentena e bloqueio de download público.

### 4) Crescimento multi-tenant
- **Risco:** consultas lentas e isolamento insuficiente.
- **Mitigação:** índices por `school_id`, políticas de autorização tenant-aware e possível particionamento futuro.

### 5) Suporte e auditoria insuficientes
- **Risco:** dificuldade de investigação de incidentes.
- **Mitigação:** logs estruturados, trilha de auditoria para ações administrativas e painéis de observabilidade.

## Critérios de aceite
- Matriz risco x impacto x mitigação aprovada.
- Plano de testes de estresse para matrícula concorrente.
- Plano de resposta a incidentes documentado.

## Dependências
- Task 02, Task 04 e Task 05.
