from sqlalchemy.orm import Session
from app.api.models import User, UserSchema
from app.api.hashing import Hasher


def post(db_session: Session, payload: UserSchema):
    user = User(user_name=payload.user_name, email=payload.email, password=Hasher.get_password_hash(payload.password))
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get(db_session: Session, id: int):
    return db_session.query(User).filter(User.id == id).first()


def get_all(db_session: Session):
    return db_session.query(User).all()


def put(db_session: Session, user: User, user_name: str, email: str, password: str):
    user.user_name = user_name
    user.email = email
    user.password = Hasher.get_password_hash(password)
    db_session.commit()
    return user


def delete(db_session: Session, id: int):
    user = db_session.query(User).filter(User.id == id).first()
    db_session.delete(user)
    db_session.commit()
    return user
