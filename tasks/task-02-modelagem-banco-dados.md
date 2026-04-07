# Task 02 — Modelar banco de dados (formulários dinâmicos, respostas e vagas)

## Objetivo
Projetar um modelo relacional multi-tenant que suporte:
1. múltiplas escolas;
2. turmas com capacidade e período letivo;
3. formulários dinâmicos por escola/período;
4. respostas de matrícula com arquivos;
5. bloqueio de vagas em concorrência alta.

## Escopo
- Definir entidades centrais e relacionamentos.
- Definir estratégia de versionamento de formulário.
- Definir mecanismo transacional para matrícula e decremento de vagas.
- Definir índices, constraints e trilhas de auditoria.

## Entidades recomendadas (alto nível)
- `tenants` (opcional, se separar org da escola)
- `schools`
- `school_users`
- `academic_terms`
- `classes` (turmas)
- `enrollment_forms`
- `enrollment_form_versions`
- `enrollment_fields`
- `enrollment_field_options`
- `public_links`
- `enrollments`
- `enrollment_answers`
- `enrollment_files`
- `audit_logs`

## Estratégia para formulários dinâmicos
### Opção recomendada (híbrida)
- Metadados estruturados em tabelas (`enrollment_fields`, `enrollment_field_options`) para governança.
- Snapshot JSON da versão do formulário em `enrollment_form_versions.schema_json` para reprodutibilidade histórica.
- Respostas em formato misto:
  - Campos indexáveis (ex.: CPF/email) em colunas dedicadas em `enrollments`.
  - Resposta completa por campo em `enrollment_answers.value_json`.

## Controle de vagas (consistência forte)
### Regra
Matrícula só confirma se `classes.confirmed_enrollments < classes.capacity` no momento da transação.

### Técnica recomendada
- Transação SQL com `SELECT ... FOR UPDATE` na turma.
- Revalidação da capacidade dentro da transação.
- Inserção de matrícula + incremento de contador confirmado.
- Commit único.

### Complementos
- Índice em `(class_id, enrollment_status)`.
- Constraint/trigger defensiva para impedir extrapolação de vagas.

## Campos de formulário e validações
Cada campo deve armazenar:
- tipo (`text`, `number`, `date`, `email`, `phone`, `select`, `multi_select`, `checkbox`, `textarea`, `file_upload`)
- `label`, `placeholder`, `required`, `display_order`
- `validation_rules` (jsonb: min/max, regex, tamanho, tipo de arquivo)
- `mask_pattern`
- `is_active`

## Auditoria
- Registrar toda alteração de schema de formulário (quem, quando, diff).
- Registrar mudança de capacidade de turma.
- Registrar tentativa de matrícula em turma lotada.

## Critérios de aceite
- DER aprovado.
- Scripts iniciais de migração versionados.
- Cenários de concorrência mapeados e testáveis.

## Dependências
- Task 01 concluída.
