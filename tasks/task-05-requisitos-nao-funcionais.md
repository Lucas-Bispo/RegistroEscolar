# Task 05 — Especificar requisitos não funcionais (segurança, performance, auditoria)

## Objetivo
Definir requisitos operacionais e de qualidade para garantir confiabilidade do sistema em produção.

## Escopo
- Segurança de aplicação e dados.
- Performance e escalabilidade.
- Auditoria, rastreabilidade e conformidade.
- SLO/SLI e observabilidade.

## Requisitos recomendados
### Segurança
- TLS obrigatório em todo tráfego.
- Criptografia em repouso para banco e storage.
- Hash forte de senhas (Argon2/Bcrypt).
- RBAC com escopo por escola.
- Rate limiting por IP e por link público.
- Proteção de upload (MIME/type, extensão, tamanho, antivírus).
- Logs sem dados sensíveis (mascarar CPF, telefone, email quando necessário).

### Performance
- P95 de APIs críticas < 300ms (sem upload).
- Renderização do formulário público < 2s em rede 4G.
- Índices planejados para consultas administrativas e conferência de vagas.
- Cache de schema publicado.

### Disponibilidade
- SLO de uptime: 99.9% mensal.
- Backups automáticos + testes de restore.
- Estratégia de disaster recovery (RPO/RTO definidos).

### Auditoria
- Trilhas imutáveis para ações administrativas críticas.
- Registro de `quem/quando/o quê` em mudanças de formulário, turmas e vagas.
- Correlação de logs por `request_id` e `trace_id`.

## Critérios de aceite
- Documento de NFR aprovado e versionado.
- Métricas e alertas mínimos configurados.
- Política de retenção de logs e backups definida.

## Dependências
- Task 01 (stack observabilidade e segurança).
