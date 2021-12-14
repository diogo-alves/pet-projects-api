from typing import List

from fastapi import APIRouter, Depends, Response, status

from app import models, schemas
from app.exceptions import PermissionDeniedError
from app.services import ProjectService

from ..dependencies import get_current_user

router = APIRouter(prefix='/projects', tags=['Projects'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ProjectOut,
    summary='Create a new project',
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'}
    },
)
def create(
    payload: schemas.ProjectIn,
    project_service: ProjectService = Depends(),
    current_user: models.User = Depends(get_current_user),
):
    return project_service.create(payload, owner_id=current_user.id)


@router.get(
    '/',
    response_model=List[schemas.ProjectOut],
    summary=('List all projects'),
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'}
    },
    dependencies=[Depends(get_current_user)],
)
def list_all(
    skip: int = 0,
    limit: int = 10,
    project_service: ProjectService = Depends(),
):
    return project_service.list(skip, limit)


@router.get(
    '/{id}',
    response_model=schemas.ProjectOut,
    summary='Retrieve a project',
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
        status.HTTP_404_NOT_FOUND: {'description': 'Not found'},
    },
    dependencies=[Depends(get_current_user)],
)
def retrieve(
    id: int,
    project_service: ProjectService = Depends(),
):
    return project_service.get_by_id(id)


@router.put(
    '/{id}',
    response_model=schemas.ProjectOut,
    summary='Update a project',
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
        status.HTTP_403_FORBIDDEN: {
            'description': (
                'Permission denied if current user is not the owner of the '
                'project or a superuser'
            )
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Not found'},
    },
)
def update(
    id: int,
    payload: schemas.ProjectIn,
    project_service: ProjectService = Depends(),
    current_user: models.User = Depends(get_current_user),
):
    project = project_service.get_by_id(id)
    if not current_user.is_superuser and project.owner_id != current_user.id:
        raise PermissionDeniedError()
    return project_service.update(project, payload)


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a project',
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
        status.HTTP_403_FORBIDDEN: {
            'description': (
                'Permission denied if current user is not the owner of the '
                'project or a superuser'
            )
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Not found'},
    },
)
def delete(
    id: int,
    project_service: ProjectService = Depends(),
    current_user: models.User = Depends(get_current_user),
):
    project = project_service.get_by_id(id)
    if not current_user.is_superuser and project.owner_id != current_user.id:
        raise PermissionDeniedError()
    project_service.delete(project)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
