# Fase 2 - Design da Arquitetura

## 1. Objetivo da fase

Nesta fase, transformamos requisitos em estrutura de software.

Em termos de engenharia de software, isso significa responder perguntas como:

- quais modulos o sistema tera;
- como eles se relacionam;
- onde cada responsabilidade deve ficar;
- como evitar acoplamento excessivo;
- como preparar o projeto para crescer sem virar um monolito confuso.

Essa fase existe porque "escrever codigo" sem arquitetura costuma gerar:

- mistura de regras de negocio com detalhes de framework;
- duplicacao de logica;
- dificuldade para testar;
- dificuldade para trocar banco, API ou adaptadores externos;
- baixa manutenibilidade.

## 2. Principios arquiteturais que vamos seguir

### 2.1 KISS

`KISS (Keep It Simple, Stupid)` significa escolher uma estrutura simples, clara e suficientemente robusta para o estagio atual do produto.

Nao vamos superengenheirar com microsservicos agora. Para este momento, o melhor caminho e um **monolito modular**.

### 2.2 DRY

`DRY (Don't Repeat Yourself)` significa evitar repeticao de logica e conhecimento.

Na arquitetura, isso aparece quando:

- centralizamos configuracoes em um modulo de `core`;
- concentramos regras de negocio em `services` ou no dominio;
- evitamos colocar validacoes duplicadas em varias rotas.

### 2.3 SOLID

Mesmo em Python, `SOLID` continua muito importante:

- **S - Single Responsibility Principle:** cada modulo, classe ou funcao deve ter uma responsabilidade clara.
- **O - Open/Closed Principle:** o sistema deve permitir extensao sem exigir alteracoes arriscadas em todo lugar.
- **L - Liskov Substitution Principle:** contratos e tipos devem ser coerentes.
- **I - Interface Segregation Principle:** dependencias pequenas e especificas sao melhores do que contratos gigantes.
- **D - Dependency Inversion Principle:** a regra de negocio deve depender de abstracoes, nao de detalhes concretos quando isso fizer sentido.

### 2.4 Coesao e acoplamento

- **Alta coesao:** cada modulo deve tratar um unico assunto de negocio.
- **Baixo acoplamento:** um modulo nao deve conhecer detalhes internos demais de outro.

Exemplo: o modulo de matriculas pode usar o modulo de turmas, mas nao deve depender de detalhes internos do banco diretamente dentro da rota HTTP.

## 3. Estilo arquitetural escolhido

### Escolha: monolito modular

Vamos adotar um **monolito modular** com camadas internas bem definidas.

Isso significa:

- uma unica aplicacao backend;
- um unico processo de deploy principal no inicio;
- separacao interna por dominio;
- possibilidade de evolucao futura sem reescrever tudo.

### Por que essa escolha faz sentido

- e mais simples para um primeiro projeto profissional em Python;
- reduz complexidade operacional inicial;
- facilita testes locais no WSL Ubuntu;
- simplifica deploy futuro em servidor Linux;
- ainda permite boa escalabilidade se o design modular for bem feito.

### Alternativa que nao escolhemos agora

**Microsservicos**

Nao escolhemos porque, apesar de escalarem bem em cenarios especificos, eles aumentam:

- complexidade de deploy;
- custo operacional;
- necessidade de observabilidade mais madura;
- dificuldade de debug;
- quantidade de integracoes e contratos distribuidos.

Para este estagio, microsservicos violariam o principio `KISS`.

## 4. Stack backend proposta

Com base nas tasks do projeto, a arquitetura backend sera orientada para:

- `Python 3.12`
- `FastAPI`
- `Pydantic`
- `SQLAlchemy 2.x`
- `Alembic`
- `PostgreSQL`
- `Redis`
- `Celery` no momento em que tarefas assincronas entrarem

### Por que isso conversa bem com Python

- `FastAPI` favorece tipagem, validacao e documentacao automatica.
- `Pydantic` ajuda a validar dados de entrada e saida com clareza.
- `SQLAlchemy` oferece um ORM maduro e flexivel.
- `Alembic` resolve versionamento de schema.

Essa combinacao ajuda a aplicar boas praticas como:

- `type hints`;
- separacao entre schema de API e modelo de persistencia;
- validacao explicita;
- testabilidade.

## 5. Estrutura de diretorios recomendada

A estrutura abaixo foi pensada para um backend Python profissional usando o padrao `src/ layout`.

```txt
registro-escolar/
  README.md
  pyproject.toml
  .gitignore
  .env.example
  docs/
    fase-01-requisitos.md
    fase-02-arquitetura.md
    adr/
      0001-monolito-modular.md
  src/
    registro_escolar/
      __init__.py
      __main__.py
      app.py
      api/
        __init__.py
        dependencies.py
        routers/
          __init__.py
          health.py
          auth.py
          schools.py
          academic_terms.py
          classes.py
          forms.py
          public_links.py
          enrollments.py
      core/
        __init__.py
        config.py
        logging.py
        security.py
        exceptions.py
      domain/
        __init__.py
        schools/
        academic_terms/
        classes/
        forms/
        enrollments/
        files/
        auth/
      infrastructure/
        __init__.py
        db/
          __init__.py
          base.py
          session.py
          models/
        repositories/
        cache/
        storage/
        queue/
      services/
        __init__.py
      schemas/
        __init__.py
      workers/
        __init__.py
  tests/
    unit/
    integration/
    contract/
```

## 6. Explicando cada camada

### `src/registro_escolar`

Usaremos o `src/ layout`, que e uma pratica profissional comum em Python.

#### Por que usar `src/ layout`

Porque ele evita um problema comum: importar codigo local sem perceber erros de empacotamento.

Sem `src/`, muitas vezes o projeto funciona "na maquina do desenvolvedor", mas quebra ao instalar ou empacotar.

### `api/`

Camada de entrada HTTP.

Responsabilidades:

- receber requisicoes;
- validar parametros de transporte;
- chamar servicos;
- devolver respostas HTTP.

O que **nao** deve acontecer aqui:

- regra de negocio complexa;
- acesso SQL direto;
- logica de transacao espalhada.

### `core/`

Camada transversal com configuracoes globais.

Responsabilidades:

- leitura de configuracao;
- logging;
- seguranca;
- excecoes da aplicacao;
- componentes reutilizaveis de infraestrutura basica.

### `domain/`

Representa o coracao do negocio.

Aqui organizaremos os contextos:

- `schools`
- `academic_terms`
- `classes`
- `forms`
- `enrollments`
- `files`
- `auth`

Em cada contexto podemos ter:

- entidades;
- enumeracoes;
- regras de negocio;
- objetos de valor;
- contratos do dominio.

Essa separacao aumenta a **coesao**, porque cada pasta fala de um assunto de negocio especifico.

### `infrastructure/`

Camada de detalhes tecnicos.

Responsabilidades:

- conexao com banco;
- implementacao de repositorios;
- cache;
- integracao com storage;
- fila assincrona;
- detalhes de persistencia.

Esse desenho reduz o acoplamento entre negocio e tecnologia concreta.

### `services/`

Camada de orquestracao de casos de uso.

Responsabilidades:

- coordenar regras entre dominio, repositorios e integracoes;
- abrir caminho para transacoes e validacoes compostas;
- expor operacoes como "publicar formulario", "gerar link", "confirmar matricula".

Em muitos projetos, essa camada e chamada de `use_cases` ou `application`.

### `schemas/`

Camada de modelos de entrada e saida da API.

Aqui usaremos modelos `Pydantic` para:

- request bodies;
- response models;
- validacoes de formato;
- contratos externos.

Isso e importante porque **schema de API nao e a mesma coisa que modelo de banco**.

Separar essas camadas evita acoplamento indevido e torna o sistema mais evolutivo.

### `workers/`

Reservado para tarefas assincronas futuras, como:

- varredura de antivirus;
- notificacoes;
- processamento de arquivos;
- relatorios.

## 7. Modulos de dominio e suas responsabilidades

### `schools`
- cadastro e contexto da escola;
- configuracoes de escopo.

### `academic_terms`
- periodos letivos;
- status e vigencia.

### `classes`
- turmas;
- capacidade;
- regras relacionadas a vagas.

### `forms`
- formularios;
- versoes publicadas;
- campos dinamicos;
- regras de validacao de schema.

### `public_links`

Mesmo que a rota fique em `api/routers/public_links.py`, o comportamento de negocio fica proximo de `forms` ou `enrollments`, conforme a implementacao.

### `enrollments`
- submissao de matricula;
- estados;
- protocolo;
- validacao final;
- consistencia de vagas.

### `files`
- metadados de upload;
- vinculacao de documentos;
- integracao com storage.

### `auth`
- autenticacao;
- autorizacao;
- RBAC por escola.

## 8. Fluxo de dependencia recomendado

Queremos manter a dependencia assim:

```txt
API -> Services -> Repositories/Infrastructure -> Database
```

E o dominio sendo protegido ao maximo de detalhes externos.

### Por que isso importa

Se a rota HTTP conhece detalhes do SQL, a aplicacao fica fortemente acoplada ao banco e mais dificil de testar.

Quando usamos camadas:

- a API testa comportamento de transporte;
- o service testa regra de negocio;
- o repository testa persistencia;
- os testes ficam mais claros.

## 9. Classes e componentes que provavelmente existirao

Ainda nao vamos implementar tudo, mas a arquitetura sugere componentes como:

- `Settings` em `core/config.py`
- `AppException` e excecoes especificas em `core/exceptions.py`
- `EnrollmentService`
- `FormPublishingService`
- `PublicLinkService`
- `ClassCapacityService`
- `EnrollmentRepository`
- `ClassRepository`
- `FormRepository`

### Por que pensar nisso agora

Porque arquitetura boa antecipa responsabilidades sem escrever codigo demais cedo.

Isso ajuda a respeitar o `Single Responsibility Principle`.

## 10. Convencoes Python que ja influenciam a arquitetura

### `__init__.py`

Marca diretorios como pacotes Python e ajuda na organizacao das importacoes.

### `__main__.py`

Permite executar o pacote com:

```bash
python -m registro_escolar
```

Isso e elegante, padronizado e util para CLI ou bootstrap local.

### `if __name__ == "__main__"`

Usamos quando um arquivo tambem pode ser executado diretamente.

No nosso caso, vamos preferir `__main__.py` e um ponto de entrada bem definido, porque isso melhora organizacao.

## 11. Logging em vez de print

Desde a arquitetura, queremos planejar `logging` e nao `print`.

### Motivo tecnico

- `print` nao e estruturado;
- nao tem niveis claros;
- nao integra bem com observabilidade;
- dificulta operacao em Linux/servidor.

Com `logging`, conseguimos trabalhar com:

- `DEBUG`
- `INFO`
- `WARNING`
- `ERROR`
- `CRITICAL`

E no futuro integrar com ferramentas de monitoramento.

## 12. Tratamento de erros

Tambem vamos desenhar excecoes customizadas.

Exemplos futuros:

- `ClassCapacityExceededError`
- `PublicLinkExpiredError`
- `UnauthorizedTenantAccessError`

### Por que isso e melhor

Excecoes especificas aumentam clareza, facilitam testes e evitam blocos `except Exception` genericos demais.

## 13. Alternativas consideradas

### Alternativa 1 - Estrutura flat simples

Exemplo:

```txt
app.py
models.py
schemas.py
database.py
utils.py
```

#### Vantagem
- muito simples no inicio.

#### Desvantagem
- escala mal;
- mistura responsabilidades;
- favorece arquivo "god object";
- prejudica coesao.

Nao foi escolhida porque o produto ja nasce com complexidade de dominio relevante.

### Alternativa 2 - Arquitetura excessivamente enterprise

Exemplo: multiplas camadas abstratas, interfaces para tudo, factories demais.

#### Vantagem
- pode ser flexivel em cenarios muito grandes.

#### Desvantagem
- aumenta custo cognitivo;
- dificulta aprendizado;
- gera boilerplate cedo.

Nao foi escolhida porque violaria `KISS`.

## 14. Decisoes especificas para Linux e WSL

- evitar caminhos fixos de Windows;
- usar configuracao por variaveis de ambiente;
- preparar comandos reprodutiveis para terminal Linux;
- futuramente usar containers para padronizar ambiente;
- manter dependencias compativeis com Ubuntu e servidor Linux.

## 15. Definicao de pronto da Fase 2

A Fase 2 estara concluida quando tivermos:

- estrutura arquitetural definida;
- divisao de modulos clara;
- camadas e responsabilidades documentadas;
- racional tecnico registrado;
- base pronta para setup do ambiente na Fase 3.

## 16. Proximo passo quando autorizado

Na Fase 3, vamos preparar o ambiente profissional do projeto Python com:

- `pyproject.toml`
- virtual environment
- `.gitignore`
- estrutura inicial em `src/`
- configuracao de dependencias
- comandos de execucao local
