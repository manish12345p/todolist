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

class TodoItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None