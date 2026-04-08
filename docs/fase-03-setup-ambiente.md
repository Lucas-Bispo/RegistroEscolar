# Fase 3 - Setup do Ambiente

## 1. Objetivo da fase

Preparar a base tecnica do projeto Python para desenvolvimento profissional, com foco em:

- reproducibilidade;
- organizacao;
- compatibilidade com WSL Ubuntu e servidor Linux;
- facilidade de manutencao futura.

## 2. Decisoes tomadas

### `pyproject.toml` em vez de `requirements.txt` como configuracao principal

Escolhemos `pyproject.toml` porque ele e o padrao moderno do ecossistema Python.

Beneficios:

- centraliza metadados do projeto;
- registra dependencias;
- permite configuracao de ferramentas como `pytest` e `ruff`;
- facilita empacotamento futuro.

O `requirements.txt` pode existir no futuro para cenarios especificos, mas o arquivo principal da configuracao sera o `pyproject.toml`.

### `src/ layout`

Escolhemos o padrao `src/` porque ele reduz erros de importacao e melhora a confiabilidade do empacotamento.

### Configuracao por variaveis de ambiente

Foi criado `.env.example` para documentar a configuracao minima da aplicacao.

Isso e importante porque:

- evita valores hardcoded;
- facilita variacao por ambiente;
- combina bem com Linux, containers e deploy futuro.

## 3. Estrutura inicial criada

```txt
src/
  registro_escolar/
    __init__.py
    __main__.py
    app.py
    api/
      router.py
      routers/
        health.py
    core/
      config.py
      logging.py
```

## 4. Ponto de entrada

O projeto agora pode ser executado como pacote Python por meio de:

```bash
python -m registro_escolar
```

Essa escolha usa `__main__.py`, o que e mais organizado do que espalhar execucao em arquivos aleatorios.

## 5. Logging

Foi preparado um modulo de logging com `logging` da biblioteca padrao.

Motivo:

- melhor observabilidade;
- niveis de log;
- integracao futura com infraestrutura Linux;
- melhor que `print` para aplicacoes reais.

## 6. O que ainda nao foi feito

Esta fase nao implementa regra de negocio.

Ela prepara a base para:

- implementacao dos modulos de dominio;
- testes;
- linting;
- empacotamento;
- deploy.

## 7. Como preparar o ambiente no WSL Ubuntu

Exemplo de fluxo recomendado:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .[dev]
python -m registro_escolar
```

## 8. Definicao de pronto da fase

A Fase 3 esta concluida quando:

- o projeto possui configuracao moderna em `pyproject.toml`;
- a aplicacao possui estrutura inicial em `src/`;
- existe ponto de entrada executavel;
- existe configuracao documentada por ambiente;
- o repositorio esta preparado para a Fase 4.
