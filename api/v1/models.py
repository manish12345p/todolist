from pydantic import BaseModel, Field
import uuid
from typing import Optional
class TodoItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    description: Optional[str] = None

class TodoItemCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None




    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Title cannot be empty.")
        return v

    @validator('description')
    def description_min_length(cls, v):
        if v is not None and len(v) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        return v

class TodoItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("Title cannot be empty.")
        return v

    @validator('description')
    def description_min_length(cls, v):
        if v is not None and len(v) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        return v
