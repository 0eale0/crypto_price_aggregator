from fastapi import APIRouter, Depends
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter, SQLAlchemyCRUDRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from api.services.db_services import get_session, create_new_user
from app.models.forms import crud
from app.models.domain import users
from app.core.permissions import is_admin

router_cryptocurrency = SQLAlchemyCRUDRouter(schema=crud.Cryptocurrency,
                                             db_model=users.Cryptocurrency,
                                             db=get_session,
                                             dependencies=[Depends(is_admin)])

router_user = SQLAlchemyCRUDRouter(schema=crud.User,
                                   db_model=users.User,
                                   db=get_session,
                                   dependencies=[Depends(is_admin)])


@router_user.post('')
def create_one(form: crud.UserCreate, db: Session = Depends(get_session)):
    try:
        user = create_new_user(form, db)
        return HTMLResponse(content="User is created", status_code=200)
    except IntegrityError as e:
        return HTMLResponse("This email or username already exists")


router_exchange = SQLAlchemyCRUDRouter(schema=crud.Exchange,
                                       db_model=users.Exchange,
                                       db=get_session,
                                       dependencies=[Depends(is_admin)])

router_coin_price = SQLAlchemyCRUDRouter(schema=crud.CoinPrice,
                                         db_model=users.CoinPrice,
                                         db=get_session,
                                         dependencies=[Depends(is_admin)])

router_user_favourite_crypto = SQLAlchemyCRUDRouter(schema=crud.UserFavouriteCrypto,
                                                    db_model=users.UserFavouriteCrypto,
                                                    db=get_session,
                                                    dependencies=[Depends(is_admin)])

router_post = SQLAlchemyCRUDRouter(schema=crud.Post,
                                   db_model=users.Post,
                                   db=get_session,
                                   dependencies=[Depends(is_admin)])

router_post_picture = SQLAlchemyCRUDRouter(schema=crud.PostPicture,
                                           db_model=users.PostPicture,
                                           db=get_session,
                                           dependencies=[Depends(is_admin)])

router_like = SQLAlchemyCRUDRouter(schema=crud.Like,
                                   db_model=users.Like,
                                   db=get_session,
                                   dependencies=[Depends(is_admin)])

router_posts_comment = SQLAlchemyCRUDRouter(schema=crud.PostsComment,
                                            db_model=users.PostsComment,
                                            db=get_session,
                                            dependencies=[Depends(is_admin)])
