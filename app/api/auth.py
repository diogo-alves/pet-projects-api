from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas
from app.core.security import generate_access_token
from app.services import AuthenticationService

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/token',
    response_model=schemas.Token,
    summary='Generate access token',
    responses={
        status.HTTP_401_UNAUTHORIZED: {'description': 'Not authenticated'},
        status.HTTP_403_FORBIDDEN: {
            'description': 'Permission denied if user is inactive'
        },
    },
)
def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(),
):
    user = auth_service.authenticate(form_data.username, form_data.password)
    claims = {'sub': user.email}
    return {
        'access_token': generate_access_token(claims),
        'token_type': 'bearer',
    }
