"""Rotas HTML do painel administrativo inicial."""

import json
from datetime import date, datetime
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from registro_escolar.dependencies import (
    get_academic_term_service,
    get_admin_auth_service,
    get_enrollment_service,
    get_enrollment_form_service,
    get_public_enrollment_link_service,
    get_school_class_service,
    get_school_service,
)
from registro_escolar.domain.forms.entities import FormField
from registro_escolar.services.academic_terms import (
    AcademicTermAlreadyExistsError,
    AcademicTermService,
    InvalidAcademicTermRangeError,
)
from registro_escolar.services.auth import AdminAuthService, AuthenticationError
from registro_escolar.services.classes import (
    InvalidClassCapacityError,
    InvalidClassRelationError,
    SchoolClassAlreadyExistsError,
    SchoolClassNotFoundError,
    SchoolClassService,
)
from registro_escolar.services.enrollments import (
    ClassCapacityExceededError,
    EnrollmentNotFoundError,
    EnrollmentService,
    EnrollmentSubmissionLimitReachedError,
    InvalidEnrollmentSubmissionError,
    InvalidEnrollmentStatusTransitionError,
)
from registro_escolar.services.forms import (
    EnrollmentFormAlreadyExistsError,
    EnrollmentFormService,
    InvalidEnrollmentFormFieldsError,
    InvalidEnrollmentFormRelationError,
)
from registro_escolar.services.public_links import (
    InvalidPublicEnrollmentLinkConfigurationError,
    InvalidPublicEnrollmentLinkRelationError,
    PublicEnrollmentLinkExpiredError,
    PublicEnrollmentLinkInactiveError,
    PublicEnrollmentLinkNotFoundError,
    PublicEnrollmentLinkService,
)
from registro_escolar.services.schools import SchoolAlreadyExistsError, SchoolService

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(tags=["web"])


def build_public_enrollment_context(
    request: Request,
    school: object,
    academic_term: object,
    enrollment_form: object,
    public_link: object,
    available_classes: object,
    error: str | None = None,
    submitted_answers: dict[int, str] | None = None,
    submitted_class_id: str | None = None,
) -> dict[str, object]:
    """Monta o contexto compartilhado da pagina publica de matricula."""

    return {
        "request": request,
        "page_title": f"Matricula | {school.name}",
        "school": school,
        "academic_term": academic_term,
        "enrollment_form": enrollment_form,
        "public_link": public_link,
        "available_classes": available_classes,
        "error": error,
        "submitted_answers": submitted_answers or {},
        "submitted_class_id": submitted_class_id or "",
    }


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
    academic_term_service: Annotated[
        AcademicTermService,
        Depends(get_academic_term_service),
    ],
    school_class_service: Annotated[
        SchoolClassService,
        Depends(get_school_class_service),
    ],
    enrollment_form_service: Annotated[
        EnrollmentFormService,
        Depends(get_enrollment_form_service),
    ],
    public_link_service: Annotated[
        PublicEnrollmentLinkService,
        Depends(get_public_enrollment_link_service),
    ],
    enrollment_service: Annotated[
        EnrollmentService,
        Depends(get_enrollment_service),
    ],
    error: str | None = None,
) -> object:
    """Renderiza o painel administrativo protegido."""

    try:
        admin_email = require_admin_session(request)
    except PermissionError:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    schools = service.list_schools()
    academic_terms = academic_term_service.list_terms()
    classes = school_class_service.list_classes()
    forms = enrollment_form_service.list_forms()
    public_links = public_link_service.list_links()
    enrollments = enrollment_service.list_enrollments()
    class_capacity = {
        school_class.id: {
            "confirmed": enrollment_service.count_confirmed_enrollments(school_class.id),
            "remaining": max(
                school_class.capacity
                - enrollment_service.count_confirmed_enrollments(school_class.id),
                0,
            ),
        }
        for school_class in classes
    }
    context = {
        "request": request,
        "schools": schools,
        "academic_terms": academic_terms,
        "classes": classes,
        "forms": forms,
        "public_links": public_links,
        "enrollments": enrollments,
        "class_capacity": class_capacity,
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


@router.post(
    "/admin/academic-terms",
    summary="Cria um periodo letivo a partir do painel web",
)
def create_academic_term_from_form(
    request: Request,
    name: Annotated[str, Form()],
    start_date: Annotated[str, Form()],
    end_date: Annotated[str, Form()],
    service: Annotated[AcademicTermService, Depends(get_academic_term_service)],
    is_active: Annotated[str | None, Form()] = None,
) -> RedirectResponse:
    """Processa o formulario de periodo letivo no painel."""

    try:
        require_admin_session(request)
    except PermissionError:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    try:
        service.create_term(
            name=name,
            start_date=date.fromisoformat(start_date),
            end_date=date.fromisoformat(end_date),
            is_active=is_active is not None,
        )
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    except (
        AcademicTermAlreadyExistsError,
        InvalidAcademicTermRangeError,
        ValueError,
    ):
        return RedirectResponse(
            url="/admin?error=Falha+ao+criar+o+periodo+letivo",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.post("/admin/classes", summary="Cria uma turma a partir do painel web")
def create_class_from_form(
    request: Request,
    school_id: Annotated[str, Form()],
    academic_term_id: Annotated[str, Form()],
    name: Annotated[str, Form()],
    shift: Annotated[str, Form()],
    capacity: Annotated[int, Form()],
    service: Annotated[SchoolClassService, Depends(get_school_class_service)],
    is_active: Annotated[str | None, Form()] = None,
) -> RedirectResponse:
    """Processa o formulario de turma e redireciona para o dashboard."""

    try:
        require_admin_session(request)
    except PermissionError:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    try:
        service.create_class(
            school_id=school_id,
            academic_term_id=academic_term_id,
            name=name,
            shift=shift,
            capacity=capacity,
            is_active=is_active is not None,
        )
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    except (
        SchoolClassAlreadyExistsError,
        InvalidClassCapacityError,
        InvalidClassRelationError,
        ValueError,
    ):
        return RedirectResponse(
            url="/admin?error=Falha+ao+criar+a+turma",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.post("/admin/forms", summary="Cria um formulario a partir do painel web")
def create_form_from_form(
    request: Request,
    school_id: Annotated[str, Form()],
    academic_term_id: Annotated[str, Form()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    fields_json: Annotated[str, Form()],
    service: Annotated[
        EnrollmentFormService,
        Depends(get_enrollment_form_service),
    ],
    is_published: Annotated[str | None, Form()] = None,
) -> RedirectResponse:
    """Processa o formulario dinamico inicial e redireciona para o dashboard."""

    try:
        require_admin_session(request)
    except PermissionError:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    try:
        parsed_fields = json.loads(fields_json)
        if not isinstance(parsed_fields, list):
            raise ValueError
        fields = [
            FormField(
                label=str(item["label"]),
                field_type=str(item["field_type"]),
                required=bool(item.get("required", True)),
                placeholder=str(item.get("placeholder", "")),
                options=tuple(str(option) for option in item.get("options", [])),
                order=int(item["order"]),
            )
            for item in parsed_fields
        ]
        service.create_form(
            school_id=school_id,
            academic_term_id=academic_term_id,
            name=name,
            description=description,
            fields=fields,
            is_published=is_published is not None,
        )
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    except (
        EnrollmentFormAlreadyExistsError,
        InvalidEnrollmentFormFieldsError,
        InvalidEnrollmentFormRelationError,
        KeyError,
        TypeError,
        ValueError,
    ):
        return RedirectResponse(
            url="/admin?error=Falha+ao+criar+o+formulario",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.post("/admin/public-links", summary="Cria um link publico a partir do painel web")
def create_public_link_from_form(
    request: Request,
    school_id: Annotated[str, Form()],
    academic_term_id: Annotated[str, Form()],
    form_id: Annotated[str, Form()],
    expires_at: Annotated[str, Form()],
    max_submissions: Annotated[int, Form()],
    service: Annotated[
        PublicEnrollmentLinkService,
        Depends(get_public_enrollment_link_service),
    ],
    is_active: Annotated[str | None, Form()] = None,
) -> RedirectResponse:
    """Processa o formulario de link publico e redireciona para o dashboard."""

    try:
        require_admin_session(request)
    except PermissionError:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    try:
        service.create_link(
            school_id=school_id,
            academic_term_id=academic_term_id,
            form_id=form_id,
            expires_at=datetime.fromisoformat(expires_at),
            max_submissions=max_submissions,
            is_active=is_active is not None,
        )
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    except (
        InvalidPublicEnrollmentLinkRelationError,
        InvalidPublicEnrollmentLinkConfigurationError,
        ValueError,
    ):
        return RedirectResponse(
            url="/admin?error=Falha+ao+criar+o+link+publico",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.post(
    "/admin/enrollments/{enrollment_id}/status",
    summary="Atualiza o status operacional de uma inscricao no painel",
)
def update_enrollment_status_from_form(
    enrollment_id: str,
    request: Request,
    new_status: Annotated[str, Form()],
    enrollment_service: Annotated[
        EnrollmentService,
        Depends(get_enrollment_service),
    ],
) -> RedirectResponse:
    """Processa a acao operacional do painel sobre uma inscricao."""

    try:
        require_admin_session(request)
    except PermissionError:
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    try:
        enrollment_service.update_status(
            enrollment_id=enrollment_id,
            new_status=new_status,
        )
        return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
    except (
        EnrollmentNotFoundError,
        InvalidEnrollmentStatusTransitionError,
        EnrollmentSubmissionLimitReachedError,
        InvalidEnrollmentSubmissionError,
        ClassCapacityExceededError,
    ):
        return RedirectResponse(
            url="/admin?error=Falha+ao+atualizar+o+status+da+inscricao",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/matricula/{token}", summary="Renderiza o formulario publico por token")
def public_enrollment_page(
    token: str,
    request: Request,
    public_link_service: Annotated[
        PublicEnrollmentLinkService,
        Depends(get_public_enrollment_link_service),
    ],
    school_service: Annotated[SchoolService, Depends(get_school_service)],
    academic_term_service: Annotated[
        AcademicTermService,
        Depends(get_academic_term_service),
    ],
    enrollment_form_service: Annotated[
        EnrollmentFormService,
        Depends(get_enrollment_form_service),
    ],
    school_class_service: Annotated[
        SchoolClassService,
        Depends(get_school_class_service),
    ],
) -> object:
    """Renderiza a primeira pagina publica da campanha de matricula."""

    try:
        public_link = public_link_service.resolve_active_link(token)
        school = school_service.get_school(public_link.school_id)
        academic_term = academic_term_service.get_term(public_link.academic_term_id)
        enrollment_form = enrollment_form_service.get_form(public_link.form_id)
        available_classes = [
            school_class
            for school_class in school_class_service.list_classes()
            if school_class.school_id == public_link.school_id
            and school_class.academic_term_id == public_link.academic_term_id
            and school_class.is_active
        ]
    except (
        PublicEnrollmentLinkNotFoundError,
        PublicEnrollmentLinkInactiveError,
        PublicEnrollmentLinkExpiredError,
    ) as exc:
        context = {
            "request": request,
            "page_title": "Link publico | RegistroEscolar",
            "error": str(exc),
        }
        return templates.TemplateResponse(request, "public_link_error.html", context)

    context = build_public_enrollment_context(
        request=request,
        school=school,
        academic_term=academic_term,
        enrollment_form=enrollment_form,
        public_link=public_link,
        available_classes=available_classes,
    )
    return templates.TemplateResponse(request, "public_enrollment_form.html", context)


@router.post("/matricula/{token}", summary="Registra a inscricao publica por token")
async def submit_public_enrollment(
    token: str,
    request: Request,
    public_link_service: Annotated[
        PublicEnrollmentLinkService,
        Depends(get_public_enrollment_link_service),
    ],
    school_service: Annotated[SchoolService, Depends(get_school_service)],
    academic_term_service: Annotated[
        AcademicTermService,
        Depends(get_academic_term_service),
    ],
    enrollment_form_service: Annotated[
        EnrollmentFormService,
        Depends(get_enrollment_form_service),
    ],
    school_class_service: Annotated[
        SchoolClassService,
        Depends(get_school_class_service),
    ],
    enrollment_service: Annotated[
        EnrollmentService,
        Depends(get_enrollment_service),
    ],
) -> object:
    """Processa a submissao publica da matricula."""

    try:
        public_link = public_link_service.resolve_active_link(token)
        school = school_service.get_school(public_link.school_id)
        academic_term = academic_term_service.get_term(public_link.academic_term_id)
        enrollment_form = enrollment_form_service.get_form(public_link.form_id)
    except (
        PublicEnrollmentLinkNotFoundError,
        PublicEnrollmentLinkInactiveError,
        PublicEnrollmentLinkExpiredError,
    ) as exc:
        context = {
            "request": request,
            "page_title": "Link publico | RegistroEscolar",
            "error": str(exc),
        }
        return templates.TemplateResponse(request, "public_link_error.html", context)

    available_classes = [
        school_class
        for school_class in school_class_service.list_classes()
        if school_class.school_id == public_link.school_id
        and school_class.academic_term_id == public_link.academic_term_id
        and school_class.is_active
    ]

    form_data = await request.form()
    class_id = str(form_data.get("class_id", "")).strip()
    submitted_answers = {
        field.order: str(form_data.get(f"field_{field.order}", ""))
        for field in enrollment_form.fields
    }

    try:
        enrollment = enrollment_service.create_public_enrollment(
            token=token,
            class_id=class_id,
            answers=submitted_answers,
        )
        school_class = school_class_service.get_class(enrollment.class_id)
    except (
        InvalidEnrollmentSubmissionError,
        EnrollmentSubmissionLimitReachedError,
        PublicEnrollmentLinkNotFoundError,
        PublicEnrollmentLinkInactiveError,
        PublicEnrollmentLinkExpiredError,
    ) as exc:
        context = build_public_enrollment_context(
            request=request,
            school=school,
            academic_term=academic_term,
            enrollment_form=enrollment_form,
            public_link=public_link,
            available_classes=available_classes,
            error=str(exc),
            submitted_answers=submitted_answers,
            submitted_class_id=class_id,
        )
        return templates.TemplateResponse(request, "public_enrollment_form.html", context)
    except SchoolClassNotFoundError:
        context = build_public_enrollment_context(
            request=request,
            school=school,
            academic_term=academic_term,
            enrollment_form=enrollment_form,
            public_link=public_link,
            available_classes=available_classes,
            error="A turma selecionada nao foi encontrada.",
            submitted_answers=submitted_answers,
            submitted_class_id=class_id,
        )
        return templates.TemplateResponse(request, "public_enrollment_form.html", context)

    context = {
        "request": request,
        "page_title": f"Protocolo | {school.name}",
        "school": school,
        "academic_term": academic_term,
        "school_class": school_class,
        "enrollment": enrollment,
    }
    return templates.TemplateResponse(request, "public_enrollment_success.html", context)


@router.post("/logout", summary="Encerra a sessao do admin")
def logout(request: Request) -> RedirectResponse:
    """Remove a sessao do admin atual."""

    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
