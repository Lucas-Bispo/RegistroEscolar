# RegistroEscolar

Plataforma SaaS de matricula online para multiplas escolas, com foco em formularios dinamicos, links publicos e controle confiavel de vagas.

## Navegacao rapida

- Documentacao central: [docs/README.md](docs/README.md)
- Visao geral do projeto: [README.md](README.md)
- Requisitos: [docs/fase-01-requisitos.md](docs/fase-01-requisitos.md)
- Arquitetura: [docs/fase-02-arquitetura.md](docs/fase-02-arquitetura.md)
- Setup do ambiente: [docs/fase-03-setup-ambiente.md](docs/fase-03-setup-ambiente.md)

## Estado atual

O projeto esta em construcao incremental seguindo fases classicas de engenharia de software.

## Documentacao disponivel

- [Central de documentacao](docs/README.md)
- [Fase 1 - Requisitos](docs/fase-01-requisitos.md)
- [Fase 2 - Arquitetura](docs/fase-02-arquitetura.md)
- [Fase 3 - Setup do ambiente](docs/fase-03-setup-ambiente.md)
- [Fase 4 - Implementacao inicial](docs/fase-04-implementacao-inicial.md)
- [Guia local de execucao](docs/runbooks/localhost.md)
- [ADR 0001 - Monolito modular](docs/adr/0001-monolito-modular.md)

## Roadmap de engenharia

1. Entendimento de requisitos e user stories
2. Design da arquitetura
3. Setup do ambiente Python
4. Implementacao
5. Documentacao
6. Testes
7. Refatoracao e boas praticas
8. Empacotamento e consideracoes de deploy

## Direcao tecnica inicial

- Backend em Python
- Desenvolvimento local em WSL Ubuntu
- Execucao futura em servidor Linux
- Arquitetura inicial em monolito modular

## Como rodar localmente

Fluxo recomendado no WSL Ubuntu:

```bash
cd /mnt/c/Users/lukao/OneDrive/Documents/RegistroEscolar
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
python -m registro_escolar
```

Depois disso, a API deve ficar disponivel em:

- `http://localhost:8000/`
- `http://localhost:8000/docs`
- `http://localhost:8000/api/v1/health`
- `http://localhost:8000/api/v1/schools`

Para um passo a passo mais completo, consulte:

- [Guia local de execucao](docs/runbooks/localhost.md)

## Observacao

A implementacao foi iniciada com um primeiro recorte vertical simples do dominio de escolas, usando armazenamento em memoria para validar a arquitetura antes da integracao com banco de dados.
