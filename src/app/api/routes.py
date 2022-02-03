from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from fastapi import BackgroundTasks, FastAPI
from app.api import services
from app.api.models import UserDB, UserSchema
from app.db import SessionLocal


router = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserDB, status_code=201)
async def create_user(*, db: Session = Depends(get_db), payload: UserSchema):
    user = services.post(db_session=db, payload=payload)
    return user


@router.get("/{id}/", response_model=UserDB)
async def read_user(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    user = services.get(db_session=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Note not found")
    return user


@router.get("/user-list", response_model=List[UserDB])
async def read_all_users(db: Session = Depends(get_db)):
    return services.get_all(db_session=db)


@router.put("/{id}/", response_model=UserDB)
async def update_user(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0), payload: UserSchema
):
    user = services.get(db_session=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = services.put(
        db_session=db, user=user, user_name=payload.user_name, email=payload.email, password=payload.password
    )
    return user


@router.delete("/{id}/", response_model=UserDB)
async def delete_user(
    *, db: Session = Depends(get_db), id: int = Path(..., gt=0),
):
    user = services.get(db_session=db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Note not found")
    user = services.delete(db_session=db, id=id)
    return user
