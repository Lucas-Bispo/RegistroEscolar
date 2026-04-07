# Task 03 — Definir estrutura de pastas limpa e escalável

## Objetivo
Propor estrutura modular para backend Python e front-end administrativo, priorizando separação de domínios e manutenibilidade.

## Escopo
- Estrutura de diretórios do backend por bounded context.
- Convenções de naming e organização de testes.
- Organização de docs e ADRs.

## Estrutura sugerida
```txt
registro-escolar/
  apps/
    api/
      src/
        main.py
        core/            # config, segurança, observabilidade
        modules/
          schools/
          classes/
          forms/
          enrollments/
          files/
          auth/
        db/
          models/
          migrations/
          repositories/
        services/
        schemas/
        workers/
      tests/
        unit/
        integration/
        contract/
    admin-web/
      src/
      tests/
  infra/
    docker/
    k8s/
    terraform/
  docs/
    adr/
    api/
    runbooks/
  tasks/
```

## Princípios organizacionais
- **Domínio primeiro**: rotas, serviços e repositórios por módulo funcional.
- **Dependência unidirecional**: API -> service -> repository -> DB.
- **Testes próximos ao comportamento**: unitário para regra, integração para banco, contrato para API.

## Critérios de aceite
- Estrutura de pastas acordada pelo time.
- Template de novos módulos definido.
- Convenções documentadas no `README`.

## Dependências
- Task 01 (stack) para consolidar ferramentas.
