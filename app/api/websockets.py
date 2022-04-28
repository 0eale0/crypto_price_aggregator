from fastapi import Depends, FastAPI, HTTPException, status
from starlette.requests import Request

sub_app_2 = FastAPI()


@sub_app_2.get('/', tags=['Main'])
async def homepage(request: Request):
    user = request.session.get('user')
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
