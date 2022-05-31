from fastapi import APIRouter, Depends
from fastapi_crudrouter import MemoryCRUDRouter as CRUDRouter, SQLAlchemyCRUDRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from app.api.services.db_services import get_session, create_new_user, get_current_active_user
from app.models.domain.users import User, Post, Like, PostsComment
from app.models.forms import crud
from app.models.domain import users
from app.core.permissions import is_admin, is_user

router_cryptocurrency = SQLAlchemyCRUDRouter(
    schema=crud.Cryptocurrency,
    db_model=users.Cryptocurrency,
    db=get_session,
    get_all_route=[Depends(is_user)],
    get_one_route=[Depends(is_user)],
    create_route=[Depends(is_admin)],
    update_route=[Depends(is_admin)],
    delete_one_route=[Depends(is_admin)],
    delete_all_route=[Depends(is_admin)],
)

router_user = SQLAlchemyCRUDRouter(
    schema=crud.User,
    db_model=users.User,
    db=get_session,
    get_all_route=[Depends(is_admin)],
    get_one_route=[Depends(is_admin)],
    create_route=[Depends(is_admin)],
    update_route=[Depends(is_admin)],
    delete_one_route=[Depends(is_admin)],
    delete_all_route=[Depends(is_admin)],
)


@router_user.post("")
def create_one(form: crud.UserCreate, db: Session = Depends(get_session)):
    try:
        user = create_new_user(form, db)
        return HTMLResponse(content="User is created", status_code=200)
    except IntegrityError as e:
        return HTMLResponse("This email or username already exists")


router_exchange = SQLAlchemyCRUDRouter(
    schema=crud.Exchange,
    db_model=users.Exchange,
    db=get_session,
    get_all_route=[Depends(is_user)],
    get_one_route=[Depends(is_user)],
    create_route=[Depends(is_admin)],
    update_route=[Depends(is_admin)],
    delete_one_route=[Depends(is_admin)],
    delete_all_route=[Depends(is_admin)],
)

router_post_topics = SQLAlchemyCRUDRouter(
    schema=crud.PostTopics,
    db_model=users.PostTopics,
    db=get_session,
    dependencies=[Depends(is_admin)],
)


router_coin_price = SQLAlchemyCRUDRouter(
    schema=crud.CoinPrice,
    db_model=users.CoinPrice,
    db=get_session,
    get_all_route=[Depends(is_user)],
    get_one_route=[Depends(is_user)],
    create_route=[Depends(is_admin)],
    update_route=[Depends(is_admin)],
    delete_one_route=[Depends(is_admin)],
    delete_all_route=[Depends(is_admin)],
)

router_user_favourite_crypto = SQLAlchemyCRUDRouter(
    schema=crud.UserFavouriteCrypto,
    db_model=users.UserFavouriteCrypto,
    db=get_session,
    get_all_route=[Depends(is_admin)],
    get_one_route=[Depends(is_admin)],
    create_route=[Depends(is_admin)],
    update_route=[Depends(is_admin)],
    delete_one_route=[Depends(is_admin)],
    delete_all_route=[Depends(is_admin)],
)

router_post = SQLAlchemyCRUDRouter(
    schema=crud.Post,
    db_model=users.Post,
    db=get_session,
    get_all_route=[Depends(is_user)],
    get_one_route=[Depends(is_user)],
    create_route=[Depends(is_user)],
    update_route=[Depends(is_user)],
    delete_one_route=[Depends(is_user)],
    delete_all_route=[Depends(is_admin)],
)


@router_post.post("")
def overloaded_create(form: crud.Post, db: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):

    if form.user_id == current_user.id:
        post = Post(user_id=form.user_id, data=form.data)
        db.add(post)
        db.commit()
        db.refresh(post)

        return HTMLResponse("Ok", status_code=200)

    else:
        return HTMLResponse("Forbidden", status_code=405)


@router_post.put("/{item_id}")
def overloaded_change(form: crud.Post, db: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):

    if form.user_id == current_user.id:
        post = db.query(Post).filter_by(id=form.id, user_id=form.user_id).one()
        post.data = form.data
        db.add(post)
        db.commit()
        db.refresh(post)

        return HTMLResponse("Ok", status_code=200)

    else:
        return HTMLResponse("Forbidden", status_code=405)


@router_post.delete("/{item_id}")
def overloaded_delete(form: crud.Post, db: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):

    if form.user_id == current_user.id:
        post = db.query(Post).filter_by(id=form.id, user_id=form.user_id).one()
        db.delete(post)
        db.commit()

        return HTMLResponse("Ok", status_code=200)

    else:
        return HTMLResponse("Forbidden", status_code=405)


router_post_picture = SQLAlchemyCRUDRouter(
    schema=crud.PostPicture,
    db_model=users.PostPicture,
    db=get_session,
    dependencies=[Depends(is_admin)],
)

router_like = SQLAlchemyCRUDRouter(
    schema=crud.Like,
    db_model=users.Like,
    db=get_session,
    get_all_route=[Depends(is_user)],
    get_one_route=[Depends(is_user)],
    create_route=[Depends(is_user)],
    update_route=[Depends(is_admin)],
    delete_one_route=[Depends(is_user)],
    delete_all_route=[Depends(is_admin)],
)


@router_like.post("")
def overloaded_create(form: crud.Like, db: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):

    if form.user_id == current_user.id:
        like = Like(user_id=form.user_id, post_id=form.post_id)
        db.add(like)
        db.commit()
        db.refresh(like)

        return HTMLResponse("Ok", status_code=200)

    else:
        return HTMLResponse("Forbidden", status_code=405)


@router_like.delete("/{item_id}")
def overloaded_delete(form: crud.Like, db: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):

    if form.user_id == current_user.id:
        like = db.query(Like).filter_by(id=form.id, user_id=form.user_id).one()
        db.delete(like)
        db.commit()

        return HTMLResponse("Ok", status_code=200)

    else:
        return HTMLResponse("Forbidden", status_code=405)


router_posts_comment = SQLAlchemyCRUDRouter(
    schema=crud.PostsComment,
    db_model=users.PostsComment,
    db=get_session,
    get_all_route=[Depends(is_user)],
    get_one_route=[Depends(is_user)],
    create_route=[Depends(is_user)],
    update_route=[Depends(is_admin)],
    delete_one_route=[Depends(is_user)],
    delete_all_route=[Depends(is_admin)],
)


@router_posts_comment.post("")
def overloaded_create(form: crud.PostsComment, db: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):

    if form.user_id == current_user.id:
        comment = PostsComment(user_id=form.user_id, post_id=form.post_id,
                               data=form.data)
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return HTMLResponse("Ok", status_code=200)

    else:
        return HTMLResponse("Forbidden", status_code=405)


@router_post.put("/{item_id}")
def overloaded_change(form: crud.PostsComment, db: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):

    if form.user_id == current_user.id:
        comment = db.query(PostsComment).filter_by(id=form.id, user_id=form.user_id).one()
        comment.data = form.data
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return HTMLResponse("Ok", status_code=200)

    else:
        return HTMLResponse("Forbidden", status_code=405)


@router_like.delete("/{item_id}")
def overloaded_delete(form: crud.PostsComment, db: Session = Depends(get_session),
                      current_user: User = Depends(get_current_active_user)):

    if form.user_id == current_user.id:
        comment = db.query(Like).filter_by(id=form.id, user_id=form.user_id).one()
        db.delete(comment)
        db.commit()

        return HTMLResponse("Ok", status_code=200)

    else:
        return HTMLResponse("Forbidden", status_code=405)