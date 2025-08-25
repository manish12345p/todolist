from fastapi.testclient import TestClient
from main import app  
import os
import json

client = TestClient(app)
device_id="test_main"
def cleanup_device_file(device_id: str):
    if os.path.exists(f'data/{device_id}.json'):
        os.remove(f'data/{device_id}.json')

def test_create_todo_item():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.post(
        "/v1/todo-item-create",
        json=[{"title": "Test Item", "description": "Test Description"}],
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Test Item"
    assert data[0]["description"] == "Test Description"
    cleanup_device_file(device_id)

def test_create_todo_item_with_string():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.post(
        "/v1/todo-item-create",
        json=[{"title": "string", "description": "string"}],
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
    cleanup_device_file(device_id)

def test_create_todo_item_with_empty_title():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.post(
        "/v1/todo-item-create",
        json=[{"title": "", "description": "Test Description"}],
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == ""
    assert data[0]["description"] == "Test Description"
    cleanup_device_file(device_id)

def test_create_todo_item_with_empty_description():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.post(
        "/v1/todo-item-create",
        json=[{"title": "Test Item", "description": ""}],
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Test Item"
    assert data[0]["description"] == ""
    cleanup_device_file(device_id)

def test_create_todo_item_with_string_title():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.post(
        "/v1/todo-item-create",
        json=[{"title": "string", "description": "Test Description"}],
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()  
    assert isinstance(data, list)
    assert data[0]["title"] == ""
    assert data[0]["description"] == "Test Description"
    cleanup_device_file(device_id)

def test_create_todo_item_with_string_description():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.post(
        "/v1/todo-item-create",
        json=[{"title": "Test Item", "description": "string"}],
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["title"] == "Test Item"
    assert data[0]["description"] == ""
    cleanup_device_file(device_id)
    
def test_get_todo_items():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.get("/v1/todo-items-read", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    cleanup_device_file(device_id)

def test_update_todo_item():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.post(
        "/v1/todo-item-create",
        json=[{"title": "Initial Item", "description": "Initial Description"}],
        headers=headers
    )
    assert response.status_code == 200
    item_id = response.json()[0]["id"]
    update_response = client.put(
        f"/v1/todo-item-update/{item_id}",
        json={"title": "Updated Item", "description": "Updated Description"},
        headers=headers
    )
    assert update_response.status_code == 200
    updated_item = update_response.json()
    assert updated_item["title"] == "Updated Item"
    assert updated_item["description"] == "Updated Description" 
    cleanup_device_file(device_id)

def test_delete_todo_item():
    cleanup_device_file(device_id)
    headers = {"Device-Id": device_id}
    response = client.post(
        "/v1/todo-item-create",
        json=[{"title": "Item to Delete", "description": "Description"}],
        headers=headers
    )
    assert response.status_code == 200
    item_id = response.json()[0]["id"]
    delete_response = client.delete(f"/v1/todo-item-delete/{item_id}", headers=headers)
    assert delete_response.status_code == 200
    data = delete_response.json()
    assert isinstance(data, list)
    assert len(data) == 0
    cleanup_device_file(device_id)