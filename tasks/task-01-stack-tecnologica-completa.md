# Task 01 — Definir stack tecnológica completa (Python) e justificativas

## Objetivo
Definir a stack base do produto SaaS de matrícula online multi-escola, com foco em escalabilidade, segurança, velocidade de desenvolvimento e operação previsível.

## Escopo
- Selecionar framework backend Python.
- Definir estratégia de API (REST + OpenAPI).
- Escolher banco de dados, ORM e migrações.
- Definir autenticação/autorização para painel administrativo.
- Definir estratégia de armazenamento de arquivos e entrega segura.
- Definir observabilidade, filas assíncronas, cache e infraestrutura de deploy.

## Decisões recomendadas (proposta base)
### Backend e API
- **Python 3.12 + FastAPI**
  - Motivo: alta produtividade, tipagem forte com Pydantic, documentação automática (OpenAPI), ótima performance para APIs.
- **Uvicorn + Gunicorn (workers Uvicorn)**
  - Motivo: padrão maduro para produção com balanceamento de workers e tuning de concorrência.

### Persistência
- **PostgreSQL 16**
  - Motivo: robustez transacional (ACID), suporte a JSONB para formulários dinâmicos, índices avançados e locking confiável para controle de vagas.
- **SQLAlchemy 2.x + Alembic**
  - Motivo: ORM maduro, padrão enterprise, migrations versionadas e seguras.

### Autenticação e autorização (admin)
- **JWT (access + refresh) + rotação de refresh token**
  - Motivo: sessão segura para SPA/painel, revogação por token family.
- **RBAC por escopo de escola (tenant-aware)**
  - Papéis mínimos: superadmin, admin_escola, operador_matricula, auditor.

### Frontend (recomendado)
- **Next.js (React) + TypeScript**
  - Motivo: produtividade, rotas robustas, ecossistema maduro para painel administrativo e formulários dinâmicos.
- **React Hook Form + Zod**
  - Motivo: forms performáticos com validação tipada consistente com backend.

### Storage de arquivos
- **S3 compatível (AWS S3, MinIO, Cloudflare R2)**
  - Motivo: escalável, resiliente e custo previsível.
- **Upload com URL pré-assinada + antivírus assíncrono (ClamAV)**
  - Motivo: reduzir carga no backend e bloquear arquivos maliciosos.

### Processamento assíncrono
- **Celery + Redis**
  - Motivo: fila para tarefas de validação de documentos, notificações, relatórios e auditorias pesadas.

### Cache e rate limit
- **Redis**
  - Motivo: cache de metadados de formulário, rate limiting por IP/link público, locks curtos para concorrência.

### Observabilidade
- **OpenTelemetry + Prometheus + Grafana + Sentry**
  - Motivo: métricas, tracing distribuído e monitoramento de erros em produção.

### Infraestrutura e DevOps
- **Docker + Docker Compose (dev) / Kubernetes ou ECS (prod)**
  - Motivo: padronização do ambiente e deploy escalável.
- **CI/CD (GitHub Actions)**
  - Pipelines: lint, testes, migração dry-run, build de imagem, deploy por ambiente.

## Critérios de aceite
- Documento de stack aprovado com trade-offs explícitos.
- Padrões de segurança e observabilidade definidos.
- Ambiente local e ambiente de produção descritos.

## Entregáveis
- ADR de arquitetura (Architecture Decision Records).
- Template `.env.example` com variáveis por serviço.
- `docker-compose.yml` para dev.

## Dependências
- Nenhuma (task inicial).
