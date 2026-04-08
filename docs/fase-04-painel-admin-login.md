# Fase 4 - Painel Admin e Login

## 1. Objetivo

Evoluir a interface web inicial para refletir melhor o fluxo real do produto:

- login administrativo;
- acesso protegido ao painel;
- preparacao para configuracao de escolas, vagas e formularios.

## 2. Motivacao de negocio

Pelos requisitos do projeto, o sistema tem dois contextos diferentes:

- painel administrativo autenticado;
- fluxo publico de matricula sem login.

Ou seja, a pagina principal do sistema nao deve ser tratada como se qualquer pessoa pudesse administrar escolas e formularios.

## 3. Decisao tecnica

Foi implementado um login web inicial baseado em sessao com cookie assinado.

### Por que esta abordagem foi escolhida agora

- e suficiente para o painel server-side atual;
- e simples de manter neste estagio;
- evita acoplamento prematuro com um frontend SPA;
- prepara o terreno para evolucao futura de autenticacao mais robusta.

## 4. Trade-off importante

O documento de stack recomenda `JWT` para um painel SPA futuro. Isso continua valido.

Entretanto, como a interface atual ainda e server-side com `Jinja2`, usar sessao com cookie assinado e um passo intermediario coerente com `KISS`.

## 5. Fluxo atual

1. Usuario acessa `/`
2. Sistema exibe tela de login
3. Credenciais validas criam sessao
4. Usuario e redirecionado para `/admin`
5. Painel mostra escolas cadastradas e proximos modulos planejados

## 6. Configuracao minima

As credenciais iniciais do admin ficam em variaveis de ambiente:

- `APP_ADMIN_EMAIL`
- `APP_ADMIN_PASSWORD`
- `APP_SECRET_KEY`

## 7. Proximo passo natural

Depois do login e painel base, os proximos modulos administrativos devem ser:

- periodos letivos;
- turmas e vagas;
- construtor de formulario dinamico;
- geracao de link publico de matricula.
