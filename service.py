from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def post_login(db: Session, username: str, password: str):

    test = aliased(models.Profile)
    query = db.query(models.Profile, test)

    query = query.join(test, and_(models.Profile.username == models.Profile.username))

    user = query.first()
    user = (
        [
            {
                "user_1": s1.to_dict() if hasattr(s1, "to_dict") else vars(s1),
                "user_2": s2.to_dict() if hasattr(s2, "to_dict") else vars(s2),
            }
            for s1, s2 in user
        ]
        if user
        else user
    )

    bs_jwt_payload = {
        "exp": int(
            (
                datetime.datetime.utcnow() + datetime.timedelta(seconds=100000)
            ).timestamp()
        ),
        "data": user,
    }

    jwt = jwt.encode(
        bs_jwt_payload,
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
        algorithm="HS256",
    )

    if username != username:

        raise HTTPException(status_code=400, detail="invalid user")
    res = {
        "get_records": user,
        "jwt": jwt,
    }
    return res


async def get_profile_user_id(db: Session, user_id: int):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.user_id == user_id))

    profile_one = query.first()

    profile_one = (
        (
            profile_one.to_dict()
            if hasattr(profile_one, "to_dict")
            else vars(profile_one)
        )
        if profile_one
        else profile_one
    )

    res = {
        "profile_one": profile_one,
    }
    return res


async def get_profile(db: Session):

    query = db.query(models.Profile)

    profile_all = query.all()
    profile_all = (
        [new_data.to_dict() for new_data in profile_all] if profile_all else profile_all
    )
    res = {
        "profile_all": profile_all,
    }
    return res


async def put_profile_user_id(
    db: Session, user_id: str, username: str, name: str, password: str, created_at: str
):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.user_id == user_id))
    profile_edited_record = query.first()

    if profile_edited_record:
        for key, value in {
            "name": name,
            "user_id": user_id,
            "password": password,
            "username": username,
            "created_at": created_at,
        }.items():
            setattr(profile_edited_record, key, value)

        db.commit()
        db.refresh(profile_edited_record)

        profile_edited_record = (
            profile_edited_record.to_dict()
            if hasattr(profile_edited_record, "to_dict")
            else vars(profile_edited_record)
        )
    res = {
        "profile_edited_record": profile_edited_record,
    }
    return res


async def delete_profile_user_id(db: Session, user_id: int):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.user_id == user_id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        profile_deleted = record_to_delete.to_dict()
    else:
        profile_deleted = record_to_delete
    res = {
        "profile_deleted": profile_deleted,
    }
    return res


async def post_profile(db: Session, raw_data: schemas.PostProfile):
    username: str = raw_data.username
    name: str = raw_data.name
    password: str = raw_data.password

    import uuid

    try:
        user_id: str = str(uuid.uuid4())
        print(user_id)
    except Exception as e:
        raise HTTPException(500, str(e))

    from datetime import (
        datetime,
    )

    try:
        UTC

        created_at: str = datetime.now(UTC).isoformat()
        print(created_at)
    except Exception as e:
        raise HTTPException(500, str(e))

    record_to_be_added = {"name": name, "password": password, "username": username}
    new_profile = models.Profile(**record_to_be_added)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    add_a_records = new_profile.to_dict()

    res = {
        "profile_inserted_record": add_a_records,
        "dzfghjg": created_at,
    }
    return res
