# Guia de Deploy em Linux

Este documento explica uma forma inicial e simples de colocar a aplicacao no ar em um servidor Linux.

## Links rapidos

- [README principal](../../README.md)
- [Central de documentacao](../README.md)
- [[fase-03-setup-ambiente]]
- [[fase-04-painel-admin-login]]
- [[fase-04-periodos-letivos]]

## Objetivo deste guia

Este guia cobre um deploy inicial simples para:

- servidor Linux Ubuntu;
- execucao com virtualenv;
- processo controlado por `systemd`;
- proxy reverso com `Nginx`.

Essa nao e a arquitetura final mais robusta possivel, mas e um caminho maduro e profissional para subir a aplicacao cedo.

## 1. Preparar o servidor

Atualize o sistema:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

Instale dependencias base:

```bash
sudo apt-get install -y python3.12 python3.12-venv nginx git
```

## 2. Obter o codigo

Exemplo:

```bash
cd /opt
sudo git clone <URL-DO-SEU-REPOSITORIO> registro-escolar
sudo chown -R $USER:$USER /opt/registro-escolar
cd /opt/registro-escolar
```

## 3. Criar a virtualenv

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## 4. Configurar o ambiente

Crie um arquivo `.env` com valores reais:

```env
APP_NAME=RegistroEscolar
APP_ENV=production
APP_HOST=127.0.0.1
APP_PORT=8000
APP_RELOAD=false
APP_LOG_LEVEL=INFO
APP_SECRET_KEY=troque-esta-chave
APP_ADMIN_EMAIL=admin@seudominio.com
APP_ADMIN_PASSWORD=troque-esta-senha
```

## 5. Testar manualmente

```bash
source .venv/bin/activate
python -m registro_escolar
```

Se tudo estiver certo, teste em:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`

## 6. Criar um servico systemd

Arquivo sugerido:

```ini
[Unit]
Description=RegistroEscolar
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/registro-escolar
EnvironmentFile=/opt/registro-escolar/.env
ExecStart=/opt/registro-escolar/.venv/bin/python -m registro_escolar
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Salve em:

```bash
sudo nano /etc/systemd/system/registro-escolar.service
```

Ative o servico:

```bash
sudo systemctl daemon-reload
sudo systemctl enable registro-escolar
sudo systemctl start registro-escolar
sudo systemctl status registro-escolar
```

## 7. Configurar o Nginx

Exemplo de configuracao:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Salve em:

```bash
sudo nano /etc/nginx/sites-available/registro-escolar
```

Ative:

```bash
sudo ln -s /etc/nginx/sites-available/registro-escolar /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 8. HTTPS

Quando o dominio estiver apontando para o servidor, use `certbot`:

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

## 9. Operacao basica

Logs do app:

```bash
sudo journalctl -u registro-escolar -f
```

Reiniciar:

```bash
sudo systemctl restart registro-escolar
```

Status do Nginx:

```bash
sudo systemctl status nginx
```

## 10. Observacao importante

Este guia serve para a fase atual do projeto. Quando evoluirmos para:

- PostgreSQL;
- Redis;
- workers;
- uploads;
- ambientes separados;

sera recomendavel complementar isso com:

- Docker Compose;
- `.env` por ambiente;
- pipeline de CI/CD;
- backup e observabilidade.
