from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import user_models, get_db


def fill():
    # get session object from generator
    db = next(get_db())
    try:
        admin_rights_id = _create_admin_access_rights(db)
    except IntegrityError:
        print("Start data1 already exist. Skipping")
        return
    user_rights = user_models.AccessRights(name='user')
    db.add(user_rights)
    admin = user_models.User(username="admin", password="admin", access_right_id=admin_rights_id)
    db.add(admin)
    db.commit()


def _create_admin_access_rights(db: Session):
    admin_rights = user_models.AccessRights(name='admin')
    db.add(admin_rights)
    db.commit()
    db.refresh(admin_rights)
    admin_rights_id = admin_rights.id
    return admin_rights_id
