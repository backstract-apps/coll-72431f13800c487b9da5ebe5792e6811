from pydantic import BaseModel,Field,field_validator

import datetime

import uuid

from typing import Any, Dict, List,Optional,Tuple

import re

class Profile(BaseModel):
    user_id: str
    username: str
    name: str
    password: str
    created_at: str


class ReadProfile(BaseModel):
    user_id: str
    username: str
    name: str
    password: str
    created_at: str
    class Config:
        from_attributes = True




class PostProfile(BaseModel):
    username: str = Field(..., max_length=100)
    name: str = Field(..., max_length=100)
    password: str = Field(..., max_length=100)

    class Config:
        from_attributes = True

