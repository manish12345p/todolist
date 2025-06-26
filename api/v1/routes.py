from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel , Field
from typing import List, Optional,Literal
import json
import uuid

router= APIRouter()
class Todolist(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str]=None
    description: Optional[str] = None
class TodolistCreate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
class TodoListResponse(BaseModel):
    status: Literal['success', 'error']
    data: List[Todolist]
class TodolistUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


@router.post("/todolist", response_model=TodoListResponse)
async def create_todolist(todolist: List[TodolistCreate]) -> TodoListResponse:
    try:
        try:
            with open('todolist.json', 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        new_data = []

        for item in todolist:

            if item.title == "string" and item.description == "string":
                return TodoListResponse(status="success", data=[Todolist(**i) for i in existing_data])

            new_item = Todolist(title=item.title, description=item.description)
            existing_data.append(new_item.model_dump())
            new_data.append(new_item)

        with open('todolist.json', 'w') as f:
            json.dump(existing_data, f, indent=4)

        return TodoListResponse(status="success", data=new_data)

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

@router.get("/todolist", response_model=TodoListResponse)
async def get_todolist() -> TodoListResponse:
    try:
        with open('todolist.json', 'r') as f:
            todolist = json.load(f)
    except FileNotFoundError:
        return TodoListResponse(status="success", data=[])
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    
    return TodoListResponse(status="success", data=[Todolist(**item) for item in todolist])
@router.put("/todolist/{id}", response_model=Todolist)
async def update_todolist(id: str, update_data: TodolistUpdate) -> Todolist:
    try:
        
        with open('todolist.json', 'r') as f:
            data = json.load(f)

        for index, item in enumerate(data):
            if item['id'] == id:
                updated_item = item.copy()
                
                update_fields = update_data.model_dump(exclude_unset=True)
                for key, value in update_fields.items():
                    if value is not None and value != "string":
                        updated_item[key] = value
                updated_item['id'] = id
                validated = Todolist(**updated_item)
                data[index] = validated.model_dump()
                with open('todolist.json', 'w') as f:
                    json.dump(data, f, indent=4)

                return validated

        raise HTTPException(status_code=404, detail="Todo item not found")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/todolist/{id}", response_model=TodoListResponse)
async def delete_todolist(id: str) -> TodoListResponse:
    try:
        with open('todolist.json', 'r') as f:
            existing_todolist = json.load(f)
        
        new_todolist = [item for item in existing_todolist if item['id'] != id]
        
        if len(new_todolist) == len(existing_todolist):
            return JSONResponse(status_code=404, content={"status": "error", "message": "Item not found"})
        
        with open('todolist.json', 'w') as f:
            json.dump(new_todolist, f, indent=4)
        
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"status": "error", "message": "File not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
    
    return TodoListResponse(status="success", data=[Todolist(**item) for item in new_todolist])
