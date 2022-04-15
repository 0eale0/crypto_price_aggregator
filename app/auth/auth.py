import os
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.schemas.token import Token
from auth.schemas.user import User
from auth.services.auth_helpers import fake_users_db, get_current_user, authenticate_user, \
    create_access_token

sub_app = FastAPI()

#TO DO: дописать
@app.route('/login')
async def login(request: Request):
    """/login маршрут перенаправит нас на сайт Google для предоставления доступа"""
    # absolute url for callback
    # we will define it below
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@sub_app.route('/auth_with_google')
async def auth_with_google(request: Request):
    """Когда вы предоставляете доступ с веб-сайта Google, Google
     перенаправит вас обратно на указанный вами redirect_uri, а именно request.url_for('auth_with_google').
    Этот код получит токен, который содержит access_token и id_token. id_token содержит информацию о пользователе,
    нам просто нужно проанализировать его, чтобы получить информацию о пользователе для входа"""
    token = await oauth.google.authorize_access_token(request)
    # <=0.15
    # user = await oauth.google.parse_id_token(request, token)
    user = token['userinfo']
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@sub_app.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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


@sub_app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@sub_app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]
