import os
from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse

from authlib.integrations.starlette_client import OAuth, OAuthError

from app.auth.services.db_services import get_session, create_new_user, change_user
from app.auth.schemas.token import Token
from app.auth.services import auth_helpers
from .forms import RegistrationForm, ChangeDataForm
from .models import User

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
    allow_headers=["*"],
)

sub_app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config(".env")
oauth = OAuth(config)

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


@sub_app.post("/register", tags=["User management"])
async def register(form: RegistrationForm, db: Session = Depends(get_session)):
    try:
        user = create_new_user(form, db)
        return HTMLResponse(content="User is created", status_code=200)
    except IntegrityError as e:
        return HTMLResponse("This email or username already exists")


@sub_app.get("/login", tags=["User management"])
async def login_via_google(request: Request):
    """
    Calls auth callback
    """
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@sub_app.get("/register")
async def register_with_google(request: Request):
    """
    :param request:
    :return:
    """
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@sub_app.get("/auth", tags=["User management"])
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

        request.session["user"] = user.dumps()
        return user

    return None


@sub_app.post("/login", response_model=Token, tags=["User management"])
async def login_for_access_token(
        request: Request,
        db: Session = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Logins through site system
    :return generated access_token
    """
    user = auth_helpers.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    request.session["user"] = user.dumps()
    access_token_expires = timedelta(
        minutes=int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    access_token = auth_helpers.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@sub_app.post("/change_data")
async def change_data(
        request: Request, form: ChangeDataForm, db: Session = Depends(get_session)
):
    try:
        user = request.session.get("user")
        if user:
            changed_user = change_user(user, form, db)
            # request.session['user'] = changed_user
            return changed_user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        return str(e)


@sub_app.get("/logout", tags=["User management"])
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")


@sub_app.get("/", tags=["User management"])
async def homepage(request: Request):
    user = request.session.get("user")
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
