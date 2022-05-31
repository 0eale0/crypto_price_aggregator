import os
from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from starlette.config import Config
from starlette.requests import Request
from starlette.responses import HTMLResponse

from authlib.integrations.starlette_client import OAuth, OAuthError

from app.api.services.db_services import (
    get_session,
    create_new_user,
    change_user,
    get_current_active_user,
)
from app.models.schemas.tokens import Token
from app.api.services import auth_helpers
from app.api.services.db_services import authenticate_user
from app.models.forms.users import RegistrationForm, ChangeDataForm, NameCryptoForm
from app.models.domain.users import User

router = APIRouter()

config = Config(".env")
oauth = OAuth(config)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


@router.post("/register")
async def register(form: RegistrationForm, db: Session = Depends(get_session)):
    try:
        user = create_new_user(form, db)
        return HTMLResponse(content="User is created", status_code=200)
    except IntegrityError as e:
        return HTMLResponse("This email or username already exists")


@router.get("/login")
async def login_via_google(request: Request):
    """
    Calls api callback
    """
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/register")
async def register_with_google(request: Request):
    """
    Redirects to Google auth page.\n
    Takes user`s credentials from his Google account and put them in DB\n
    """
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google")
async def auth(request: Request, db: Session = Depends(get_session)):
    """
    Handle authentication callback\n
    :param db:
    :param request: Request\n
    :return User information from Google:
    """

    try:
        full_user_info = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f"<h1>{error.description}</h1>")
    short_user_info = full_user_info.get("userinfo")

    if short_user_info:
        name = short_user_info["name"]
        email = short_user_info["email"]

        user = db.query(User).filter(User.email == email).first()
        if not user:
            user_form = User(email=email, username=name)

            user = create_new_user(user_form, db, is_google=True)

        return user

    return None


@router.post("/token", response_model=Token)
async def login_for_access_token(
    db: Session = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
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

    access_token_expires = timedelta(
        minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = auth_helpers.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/change_data")
async def change_data(
    form: ChangeDataForm,
    db: Session = Depends(get_session),
    user: User = Depends(get_current_active_user),
):
    """
    Page of changing user`s credentials.
    param: db: DB connection
    param: user: current_user(JWT token)
    """
    try:
        changed_user = change_user(user, form, db)
        return changed_user
    except Exception as e:
        return str(e)


@router.get("/home_page")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Main page. Shows just user`s credentials.\n
    param: current_user: JWT token in Authorization header.
    """
    return current_user
