import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session
from app import crud, schemas
from app.models import Item

@pytest.fixture(autouse=True)
def clean_db(test_db):
    # Clean before test
    test_db.execute(text("DELETE FROM items"))
    test_db.commit()
    yield
    # Clean after test
    test_db.execute(text("DELETE FROM items"))
    test_db.commit()

def test_create_item(test_db: Session):
    item_data = schemas.ItemCreate(
        name="Test Item",
        description="Test Description"
    )
    item = crud.create_item(test_db, item_data)
    assert item.name == "Test Item"
    assert item.description == "Test Description"
    assert item.id is not None

def test_get_item(test_db: Session):
    # Create test item
    item_data = schemas.ItemCreate(
        name="Test Item",
        description="Test Description"
    )
    created_item = crud.create_item(test_db, item_data)
    
    # Test getting the item
    item = crud.get_item(test_db, created_item.id)
    assert item is not None
    assert item.name == "Test Item"
    assert item.description == "Test Description"

def test_get_items(test_db: Session):
    # Create multiple test items
    items_data = [
        schemas.ItemCreate(name="Item 1", description="Description 1"),
        schemas.ItemCreate(name="Item 2", description="Description 2"),
        schemas.ItemCreate(name="Item 3", description="Description 3")
    ]
    for item_data in items_data:
        crud.create_item(test_db, item_data)
    
    # Test getting all items
    items = crud.get_items(test_db, skip=0, limit=100)
    assert len(items) == 3
    assert items[0].name == "Item 1"
    assert items[1].name == "Item 2"
    assert items[2].name == "Item 3"

def test_update_item(test_db: Session):
    # Create test item
    item_data = schemas.ItemCreate(
        name="Original Name",
        description="Original Description"
    )
    created_item = crud.create_item(test_db, item_data)
    
    # Update the item
    update_data = schemas.ItemUpdate(
        name="Updated Name",
        description="Updated Description"
    )
    updated_item = crud.update_item(test_db, created_item.id, update_data)
    
    assert updated_item is not None
    assert updated_item.name == "Updated Name"
    assert updated_item.description == "Updated Description"

def test_delete_item(test_db: Session):
    # Create test item
    item_data = schemas.ItemCreate(
        name="Test Item",
        description="Test Description"
    )
    created_item = crud.create_item(test_db, item_data)
    
    # Delete the item
    success = crud.delete_item(test_db, created_item.id)
    assert success is True
    
    # Verify item is deleted
    deleted_item = crud.get_item(test_db, created_item.id)
    assert deleted_item is None

def test_delete_nonexistent_item(test_db: Session):
    # Try to delete an item that doesn't exist
    success = crud.delete_item(test_db, 999)
    assert success is False

def test_update_nonexistent_item(test_db: Session):
    # Try to update an item that doesn't exist
    update_data = schemas.ItemUpdate(
        name="Updated Name",
        description="Updated Description"
    )
    updated_item = crud.update_item(test_db, 999, update_data)
    assert updated_item is None

def test_partial_update_item(test_db: Session):
    # Create test item
    item_data = schemas.ItemCreate(
        name="Original Name",
        description="Original Description"
    )
    created_item = crud.create_item(test_db, item_data)
    
    # Update only the name
    update_data = schemas.ItemUpdate(name="Updated Name")
    updated_item = crud.update_item(test_db, created_item.id, update_data)
    
    assert updated_item is not None
    assert updated_item.name == "Updated Name"
    assert updated_item.description == "Original Description"

def test_get_item_not_found(test_db: Session):
    # Try to get an item that doesn't exist
    item = crud.get_item(test_db, 999)
    assert item is None

def test_get_items_empty(test_db: Session):
    # Test getting items when database is empty
    items = crud.get_items(test_db, skip=0, limit=100)
    assert len(items) == 0

def test_get_items_pagination(test_db: Session):
    # Create multiple test items
    items_data = [
        schemas.ItemCreate(name=f"Item {i}", description=f"Description {i}")
        for i in range(1, 11)  # Create 10 items
    ]
    for item_data in items_data:
        crud.create_item(test_db, item_data)
    
    # Test pagination
    items_page1 = crud.get_items(test_db, skip=0, limit=5)
    items_page2 = crud.get_items(test_db, skip=5, limit=5)
    
    assert len(items_page1) == 5
    assert len(items_page2) == 5
    assert items_page1[0].name == "Item 1"
    assert items_page2[0].name == "Item 6"