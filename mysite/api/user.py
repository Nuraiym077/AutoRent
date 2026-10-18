from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from mysite.database.db import SessionLocal
from mysite.database.models import UserProfile
from mysite.database.schema import UserProfileOut, UserProfileCreate, UserProfileUpdate, ChatSchema, ResponseSchema

api_router = APIRouter(prefix="/api", tags=["UserProfile"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@api_router.post('/', response_model=UserProfileOut)
async def create_user(user: UserProfileCreate, db: Session = Depends(get_db)):
    user_db = UserProfile(**user.model_dump())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@api_router.get('/', response_model=List[UserProfileOut])
async def list_user(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@api_router.get('/{user_id}', response_model=UserProfileOut)
async def detail_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Профиль табылган жок")
    return user_db

@api_router.patch('/{user_id}', response_model=dict)
async def update_user(user_id: int, user: UserProfileUpdate, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Профиль табылган жок")

    for key, value in user.dict().items():
        setattr(user_db, key, value)

    db.commit()
    db.refresh(user_db)
    return {"message": "Профиль изменено"}

@api_router.delete('/{user_id}', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Профиль табылган жок")
    db.delete(user_db)
    db.commit()
    return {"message": "Профиль удалено"}


    

