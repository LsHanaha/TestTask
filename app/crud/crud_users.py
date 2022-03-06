import asyncio
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from app.schemas import user_schemas
from app.models import user_models


def _get_list_of_users(my_user_id: int, db: Session):
    # in production I am not using f-strings to pass a variable because
    # of security reasons
    sql = text(f"""
        SELECT users.id as id, username, password, name as access_right
        FROM public.users 
        JOIN public.access_rights as ar
        ON users.access_right_id = ar.id
        WHERE users.id != {my_user_id};
    """)

    query_result = db.execute(sql)
    result = []
    for row in query_result:
        result.append(row._mapping)
    return result


async def get_list_of_users(my_user_id: int, db: Session):
    loop = asyncio.get_running_loop()
    # for a long time wanted to try run_in_executor for a blocking call
    res = await loop.run_in_executor(None, _get_list_of_users, my_user_id, db)
    return res


def get_access_right_id(access_right_name: str, db: Session):
    access_right = db.query(user_models.AccessRights)\
        .filter(user_models.AccessRights.name == access_right_name)\
        .first()
    if not access_right:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No such access right as {access_right_name}")
    return access_right.id


def create_new_user(user: user_schemas.UserCreation, db: Session) \
        -> user_schemas.UserFull:
    # still prefer to use blocking version of sqlalchemy, that's why all db queries is
    # in blocking format

    access_right_id = get_access_right_id(user.access, db)
    new_user = user_models.User(
        username=user.username,
        password=user.password,
        access_right_id=access_right_id
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User '{user.username}' already exist")
    return new_user


def update_user(user: user_schemas.UserUpdate, db: Session) -> bool:

    access_right_id = get_access_right_id(user.access, db)

    try:
        db.query(user_models.User).filter(user_models.User.id == user.id)\
            .update({'username': user.username, 'access_right_id': access_right_id})
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User '{user.username}' already exist")
    return True


def delete_user(user_id: int, db: Session) -> bool:
    db.query(user_models.User).filter(user_models.User.id == user_id).delete()
    db.commit()
    return True
