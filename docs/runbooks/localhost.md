# Guia Local de Execucao

Este runbook explica como executar, validar e parar a aplicacao localmente no WSL Ubuntu.

## Links rapidos

- [README principal](../../README.md)
- [Central de documentacao](../README.md)
- [[fase-03-setup-ambiente]]
- [[fase-04-implementacao-inicial]]
- [[fase-04-interface-web]]

## Enderecos atuais

- Aplicacao raiz: `http://localhost:8000/` interface web HTML
- Swagger UI: `http://localhost:8000/docs`
- Healthcheck: `http://localhost:8000/api/v1/health`
- Escolas: `http://localhost:8000/api/v1/schools`

## Subir a aplicacao no WSL

```bash
cd /mnt/c/Users/lukao/OneDrive/Documents/RegistroEscolar
source .venv/bin/activate
python -m registro_escolar
```

## Subir em background

```bash
cd /mnt/c/Users/lukao/OneDrive/Documents/RegistroEscolar
mkdir -p .runtime
source .venv/bin/activate
APP_RELOAD=false nohup python -m registro_escolar > .runtime/server.log 2>&1 < /dev/null &
echo $! > .runtime/server.pid
```

## Ver logs

```bash
cd /mnt/c/Users/lukao/OneDrive/Documents/RegistroEscolar
cat .runtime/server.log
```

## Parar a aplicacao

```bash
cd /mnt/c/Users/lukao/OneDrive/Documents/RegistroEscolar
kill "$(cat .runtime/server.pid)"
```

## Observacao

Neste momento, o servidor ja foi validado localmente com sucesso em `localhost:8000`.
