import enum
import os
from datetime import timedelta
from pprint import pprint

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth, OAuthError

from auth.services.db_services import get_session, create_new_user
from auth.services.db_services import find_user_by_email, find_user_by_username
from auth.schemas.token import Token
from auth.services.auth_helpers import authenticate_user, create_access_token, get_password_hash
from sqlalchemy.orm import Session
from .forms import RegistrationForm

sub_app = FastAPI()
origins = [
    "http://127.0.0.1:8000/",
    "https://127.0.0.1:8000/",
]
sub_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

sub_app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config('.env')
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@sub_app.post("/register", tags=['User management'])
async def register(form: RegistrationForm, db: Session = Depends(get_session)):
    try:
        if find_user_by_username(form.username, db) and find_user_by_email(form.email, db):
            return {'message': f"User with such email and username exists"}
        elif find_user_by_email(form.email, db):
            return {'message': f"User with {form.email} email exists"}
        elif find_user_by_username(form.username, db):
            return {'message': f"User with {form.username} username exists"}
        else:
            if not form.username_length_is_valid():
                return {"message": "Username should be at least 3 symbols"}
            elif not form.password_length_is_valid():
                return {"message": "Password length should be at least 4 symbols"}
            elif not form.passwords_equal_is_valid():
                return {"message": "Check passwords"}
            else:
                user = create_new_user(form, db)
                return user

    except Exception as e:
        return str(e)


@sub_app.post("/login", response_model=Token, tags=['User management'])
async def login_for_access_token(db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Logins through site system
    :return generated access_token
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@sub_app.get('/login', tags=['User management'])
async def login_via_google(request: Request):
    """
    Calls auth callback
    """
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@sub_app.get('/auth', tags=['User management'])
async def auth(request: Request):
    """
    Handle authentication callback\n
    :param request: Request\n
    :return User information from Google:
    """
    try:
        user_info = await oauth.google.authorize_access_token(request)
        pprint(user_info)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.description}</h1>')
    user = user_info.get('userinfo')

    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@sub_app.get('/logout', tags=['User management'])
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


@sub_app.get('/', tags=['User management'])
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
