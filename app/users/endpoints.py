from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy.orm import Session

from app.schemas import user_schemas
from app.models import get_db, user_models
from app.crud import crud_users
from app.oauth2 import create_access_token, get_current_user


router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={404: {"description": "Not found"}}
)


@router.post("/login", response_model=user_schemas.Token)
def login(user_credentials: user_schemas.UserAuth, db: Session = Depends(get_db)):
    user = db.query(user_models.User)\
        .filter(user_models.User.username == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Username or email not correct")
    access_token = create_access_token({"user_id": user.id, "access_rights": user.access_rights.name})
    return {'token': access_token, 'token_type': 'bearer'}


@router.put('/')
def update_user(user: user_schemas.UserUpdate,
                current_user: user_schemas.UserFull = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if current_user.access_rights.name != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admin can perform such operation!")

    op_status = crud_users.update_user(user, db)
    return JSONResponse({'status': op_status})


@router.delete("/{user_id}")
def delete_user(user_id: int,
                current_user: user_schemas.UserFull = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if current_user.access_rights.name != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admin can perform such operation!")
    op_status = crud_users.delete_user(user_id, db)
    return JSONResponse({'status': op_status})


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserBase)
def create_user(new_user: user_schemas.UserCreation,
                current_user: user_schemas.UserFull = Depends(get_current_user),
                db: Session = Depends(get_db)):
    if current_user.access_rights.name != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only admin can perform such operation!")
    new_user = crud_users.create_new_user(new_user, db)
    return new_user


@router.get('/', response_model=List[user_schemas.UserResponse])
async def get_all_users(current_user: user_schemas.UserFull = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await crud_users.get_list_of_users(current_user.id, db)
    return data
