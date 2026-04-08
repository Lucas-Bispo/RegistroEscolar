"""Rotas HTML do painel administrativo inicial."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from registro_escolar.dependencies import get_admin_auth_service, get_school_service
from registro_escolar.services.auth import AdminAuthService, AuthenticationError
from registro_escolar.services.schools import SchoolAlreadyExistsError, SchoolService

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(tags=["web"])


def require_admin_session(request: Request) -> str:
    """Garante que exista uma sessao administrativa valida."""

    admin_email = request.session.get("admin_email")
    if not isinstance(admin_email, str) or not admin_email:
        msg = "Autenticacao necessaria."
        raise PermissionError(msg)
    return admin_email


@router.get("/", summary="Renderiza a pagina de login do painel")
def login_page(
    request: Request,
    error: str | None = None,
) -> object:
    """Renderiza a tela inicial de autenticacao do painel."""

    if request.session.get("admin_email"):
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)

    context = {
        "request": request,
        "error": error,
        "page_title": "Login | RegistroEscolar",
    }
    return templates.TemplateResponse(request, "login.html", context)

@router.post("/login", summary="Autentica o admin do painel")
def login(
    request: Request,
    email: Annotated[str, Form()],
    password: Annotated[str, Form()],
    auth_service: Annotated[AdminAuthService, Depends(get_admin_auth_service)],
) -> RedirectResponse:
    """Autentica o admin e cria a sessao web."""

    try:
        admin_email = auth_service.authenticate(email=email, password=password)
        request.session["admin_email"] = admin_email
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    except AuthenticationError:
        return RedirectResponse(
            url="/?error=Credenciais+invalidas",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/admin", summary="Renderiza o painel administrativo inicial")
def admin_dashboard(
    request: Request,
    service: Annotated[SchoolService, Depends(get_school_service)],
    error: str | None = None,
) -> object:
    """Renderiza o painel administrativo protegido."""

    try:
        admin_email = require_admin_session(request)
    except PermissionError:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    schools = service.list_schools()
    context = {
        "request": request,
        "schools": schools,
        "error": error,
        "page_title": "Painel Admin | RegistroEscolar",
        "admin_email": admin_email,
    }
    return templates.TemplateResponse(request, "admin_dashboard.html", context)


@router.post("/admin/schools", summary="Cria uma escola a partir do painel web")
def create_school_from_form(
    request: Request,
    name: Annotated[str, Form()],
    city: Annotated[str, Form()],
    state: Annotated[str, Form()],
    service: Annotated[SchoolService, Depends(get_school_service)],
) -> RedirectResponse:
    """Processa o formulario do painel e redireciona para o dashboard."""

    try:
        require_admin_session(request)
    except PermissionError:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    try:
        service.create_school(name=name, city=city, state=state)
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    except SchoolAlreadyExistsError:
        return RedirectResponse(
            url="/admin?error=Ja+existe+uma+escola+com+esse+nome",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.post("/logout", summary="Encerra a sessao do admin")
def logout(request: Request) -> RedirectResponse:
    """Remove a sessao do admin atual."""

    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
