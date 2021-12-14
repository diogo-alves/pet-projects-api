from typing import List

from fastapi import APIRouter, Depends, Response, status

from app import models, schemas
from app.services import UserService

from ..dependencies import get_current_superuser, get_current_user

router = APIRouter(prefix='/users', tags=['Users'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
    summary='Register a new user',
)
def register(payload: schemas.UserIn, user_service: UserService = Depends()):
    return user_service.create(payload)


@router.get(
    '/',
    response_model=List[schemas.UserOut],
    summary='List all users',
    dependencies=[Depends(get_current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
        status.HTTP_403_FORBIDDEN: {
            'description': (
                'Permission denied if current user is not a superuser'
            )
        },
    },
)
def list_all(
    skip: int = 0,
    limit: int = 10,
    user_service: UserService = Depends(),
):
    return user_service.list(skip, limit)


@router.get(
    '/me',
    response_model=schemas.UserOut,
    summary='Retrieve current logged user',
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
    },
)
def retrieve_logged(
    current_user: models.User = Depends(get_current_user),
):
    return current_user


@router.put(
    '/me',
    response_model=schemas.UserOut,
    summary='Update current logged user',
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
    },
)
def update_logged(
    payload: schemas.UserIn,
    user_service: UserService = Depends(),
    current_user: models.User = Depends(get_current_user),
):
    return user_service.update(current_user, payload)


@router.delete(
    '/me',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete current logged user',
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
    },
)
def delete_logged(
    user_service: UserService = Depends(),
    current_user: models.User = Depends(get_current_user),
):
    user_service.delete(current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    '/{id}',
    response_model=schemas.UserOut,
    summary='Retrieve an user',
    dependencies=[Depends(get_current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
        status.HTTP_403_FORBIDDEN: {
            'description': (
                'Permission denied if current user is not a superuser'
            )
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Not found'},
    },
)
def retrieve(
    id: int,
    user_service: UserService = Depends(),
):
    return user_service.get_by_id(id)


@router.put(
    '/{id}',
    response_model=schemas.UserOut,
    summary='Update an user',
    dependencies=[Depends(get_current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
        status.HTTP_403_FORBIDDEN: {
            'description': (
                'Permission denied if current user is not a superuser'
            )
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Not found'},
    },
)
def update(
    id: int,
    payload: schemas.FullUserIn,
    user_service: UserService = Depends(),
):
    return user_service.update_by_id(id, payload)


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete an user',
    dependencies=[Depends(get_current_superuser)],
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
        status.HTTP_403_FORBIDDEN: {
            'description': (
                'Permission denied if current user is not a superuser'
            )
        },
        status.HTTP_404_NOT_FOUND: {'description': 'Not found'},
    },
)
def delete(
    id: int,
    user_service: UserService = Depends(),
):
    user_service.delete_by_id(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
