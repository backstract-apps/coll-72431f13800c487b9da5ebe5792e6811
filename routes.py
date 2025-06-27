from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile,Query, Form
from sqlalchemy.orm import Session
from typing import List,Annotated
import service, models, schemas
from fastapi import Query
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/login')
async def post_login(username: Annotated[str, Query(max_length=100)], password: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.post_login(db, username, password)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/profile/user_id')
async def get_profile_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return await service.get_profile_user_id(db, user_id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get('/profile/')
async def get_profile(db: Session = Depends(get_db)):
    try:
        return await service.get_profile(db)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.put('/profile/user_id/')
async def put_profile_user_id(user_id: Annotated[str, Query(max_length=100)], username: Annotated[str, Query(max_length=100)], name: Annotated[str, Query(max_length=100)], password: Annotated[str, Query(max_length=100)], created_at: Annotated[str, Query(max_length=100)], db: Session = Depends(get_db)):
    try:
        return await service.put_profile_user_id(db, user_id, username, name, password, created_at)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.delete('/profile/user_id')
async def delete_profile_user_id(user_id: int, db: Session = Depends(get_db)):
    try:
        return await service.delete_profile_user_id(db, user_id)
    except Exception as e:
        raise HTTPException(500, str(e))

@router.post('/profile/')
async def post_profile(raw_data: schemas.PostProfile, db: Session = Depends(get_db)):
    try:
        return await service.post_profile(db, raw_data)
    except Exception as e:
        raise HTTPException(500, str(e))

