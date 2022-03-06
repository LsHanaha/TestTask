from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from app.models import get_db
from app.config import settings
from app.models import user_models
from app.schemas import user_schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


# Refresh token not added. Token will be expired within 1 hour
def create_access_token(data: dict) -> str:
    expire = datetime.utcnow() + timedelta(minutes=60)
    data.update({"exp": expire})
    token = jwt.encode(data, settings.oauth_key)
    return token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) \
        -> user_schemas.UserFull:
    try:
        token_data = jwt.decode(token, settings.oauth_key)
        user_id = token_data['user_id']
        user = db.query(user_models.User).filter(user_models.User.id == user_id).first()
        return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="User or password not correct",
                            headers={'WWW-Authenticate': "Bearer"})
