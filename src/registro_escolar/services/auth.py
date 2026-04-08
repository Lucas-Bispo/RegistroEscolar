"""Servicos de autenticacao web inicial do painel administrativo."""

from secrets import compare_digest

from registro_escolar.core.config import get_settings


class AuthenticationError(ValueError):
    """Erro levantado quando as credenciais informadas sao invalidas."""


class AdminAuthService:
    """Valida as credenciais iniciais do painel administrativo.

    Nesta fase usamos credenciais vindas de variaveis de ambiente como
    bootstrap simples. Em producao, a evolucao natural e migrar para
    usuarios persistidos com senha fortemente protegida.
    """

    def authenticate(self, email: str, password: str) -> str:
        """Valida email e senha e retorna o identificador do admin."""

        settings = get_settings()
        normalized_email = email.strip().lower()
        configured_email = settings.admin_email.strip().lower()

        is_email_valid = compare_digest(normalized_email, configured_email)
        is_password_valid = compare_digest(password, settings.admin_password)

        if not (is_email_valid and is_password_valid):
            msg = "Email ou senha invalidos."
            raise AuthenticationError(msg)

        return normalized_email
