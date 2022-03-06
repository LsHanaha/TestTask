from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship


from app.models import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False, unique=True)
    # plain password row only because it's not an app for production
    password = Column(Text, nullable=False)
    access_right_id = Column(Integer, ForeignKey("access_rights.id"), nullable=False, default=2)

    access_rights = relationship("AccessRights")


class AccessRights(Base):
    __tablename__ = 'access_rights'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
