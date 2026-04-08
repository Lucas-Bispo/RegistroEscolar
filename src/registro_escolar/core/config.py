"""Configuracao central da aplicacao via variaveis de ambiente."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Representa a configuracao tipada da aplicacao.

    Usamos ``BaseSettings`` para ler configuracoes de ambiente com seguranca
    e clareza, evitando valores hardcoded no codigo.
    """

    app_name: str = "RegistroEscolar"
    app_env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """Retorna uma instancia unica e cacheada das configuracoes.

    O cache reduz leituras repetidas de ambiente e centraliza a fonte
    de verdade de configuracao durante o ciclo de vida do processo.
    """

    return Settings()
