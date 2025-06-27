from pydantic import BaseModel, Field
import uuid
from typing import Optional
class Todolist(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    description: Optional[str] = None

class TodolistCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TodolistUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None