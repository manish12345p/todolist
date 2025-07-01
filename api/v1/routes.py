import os
from api.v1.models import TodoItem, TodoItemCreate, TodoItemUpdate
from fastapi import APIRouter, HTTPException , Request
from fastapi.responses import JSONResponse

from typing import List
import json
router = APIRouter()
@router.post("/todo-item-create", response_model=List[TodoItem])
async def create_todo_item(request: Request ,todo_item: List[TodoItemCreate]) -> List[TodoItem]:
    try:
        device_id=request.headers.get("Device-Id")
        if not device_id:
            raise HTTPException(status_code=400, detail="Missing Device-ID in header")
        if not os.path.exists(f'data/{device_id}.json'):
            with open(f'data/{device_id}.json', 'w') as f:
                json.dump([], f, indent=4)
        try:
            with open(f'data/{device_id}.json', 'r') as f:
                existing_data = json.load(f)
        except FileNotFoundError:
            existing_data = []

        new_data = []

        for item in todo_item:
            if item.title == "string" and item.description == "string":
                return [TodoItem(**i) for i in existing_data]
            elif item.title == "string" and item.description != "string":
                item.title = ""
            elif item.title != "string" and item.description == "string":
                item.description = ""
            new_item = TodoItem(title=item.title, description=item.description)
            existing_data.append(new_item.model_dump())
            new_data.append(new_item)

        with open(f'data/{device_id}.json', 'w') as f:
            json.dump(existing_data, f, indent=4)

        return new_data

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/todo-items-read", response_model=List[TodoItem])
async def get_todo_items(request: Request) -> List[TodoItem]:
    try:
        device_id=request.headers.get("Device-Id")
        if not device_id:
            raise HTTPException(status_code=400, detail="Missing Device-ID in header")
        if not os.path.exists(f'data/{device_id}.json'):
            with open(f'data/{device_id}.json', 'w') as f:
                json.dump([], f, indent=4)
        with open(f'data/{device_id}.json', 'r') as f:
            todolist = json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    
    return [TodoItem(**item) for item in todolist]


@router.put("/todo-item-update/{id}", response_model=TodoItem)
async def update_todo_item(request: Request,id: str, update_data: TodoItemUpdate) -> TodoItem:
    try:
        device_id=request.headers.get("Device-Id")
        if not device_id:
            raise HTTPException(status_code=400, detail="Missing Device-ID in header")  
        with open(f'data/{device_id}.json', 'r') as f:
            data = json.load(f)

        for index, item in enumerate(data):
            if item['id'] == id:
                updated_item = item.copy()
                update_fields = update_data.model_dump(exclude_unset=True)
                for key, value in update_fields.items():
                    if value is not None and value != "string":
                        updated_item[key] = value
                updated_item['id'] = id
                validated = TodoItem(**updated_item)
                data[index] = validated.model_dump()

                with open(f'data/{device_id}.json', 'w') as f:
                    json.dump(data, f, indent=4)

                return validated

        raise HTTPException(status_code=404, detail="Todo item not found")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/todo-item-delete/{id}", response_model=List[TodoItem])
async def delete_todo_item(request: Request,id: str) -> List[TodoItem]:
    try:
        device_id=request.headers.get("Device-Id")
        if not device_id:
            raise HTTPException(status_code=400, detail="Missing Device-ID in header")
        with open(f'data/{device_id}.json', 'r') as f:
            existing_todolist = json.load(f)
        
        new_todolist = [item for item in existing_todolist if item['id'] != id]
        
        if len(new_todolist) == len(existing_todolist):
            return JSONResponse(status_code=404, content={"message": "Item not found"})

        with open(f'data/{device_id}.json', 'w') as f:
            json.dump(new_todolist, f, indent=4)

    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"message": "File not found"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

    return [TodoItem(**item) for item in new_todolist]