"""Rotas HTML da interface web inicial."""

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from registro_escolar.dependencies import get_school_service
from registro_escolar.services.schools import SchoolAlreadyExistsError, SchoolService

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(tags=["web"])


@router.get("/", summary="Renderiza a pagina inicial do sistema")
def home(
    request: Request,
    service: Annotated[SchoolService, Depends(get_school_service)],
    error: str | None = None,
) -> object:
    """Renderiza a pagina inicial com escolas e formulario.

    A interface HTML usa o mesmo servico da API para evitar duplicacao
    de regra de negocio, o que reforca o principio DRY.
    """

    schools = service.list_schools()
    context = {
        "request": request,
        "schools": schools,
        "error": error,
        "page_title": "RegistroEscolar",
    }
    return templates.TemplateResponse(request, "home.html", context)


@router.post("/schools", summary="Cria uma escola a partir da interface web")
def create_school_from_form(
    name: Annotated[str, Form()],
    city: Annotated[str, Form()],
    state: Annotated[str, Form()],
    service: Annotated[SchoolService, Depends(get_school_service)],
) -> RedirectResponse:
    """Processa o formulario HTML e redireciona de volta para a home."""

    try:
        service.create_school(name=name, city=city, state=state)
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    except SchoolAlreadyExistsError:
        return RedirectResponse(
            url="/?error=Ja+existe+uma+escola+com+esse+nome",
            status_code=status.HTTP_303_SEE_OTHER,
        )
