# FastAPI CRUD Application

This is a FastAPI application that implements CRUD operations with PostgreSQL database integration.

![Application Architecture](https://github.com/majnikool/test-app-std/blob/main/test-app.jpg?raw=true)


## Features
- CRUD operations for items
- PostgreSQL database integration
- Environment variable configuration
- Logging
- Automatic database table creation
- Unit tests

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3.create a test postgres instance:

# Create a Docker network (optional but good practice)
docker network create fastapi-net

# Run PostgreSQL container
docker run --name postgres-db \
  --network fastapi-net \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -p 5432:5432 \
  -d postgres:15

# Connect to PostgreSQL container
docker exec -it postgres-db bash

# Connect to PostgreSQL
psql -U myuser -d mydatabase

#Useful Docker commands for troubleshooting:

# View container logs
docker logs postgres-db

# Stop the container
docker stop postgres-db

# Remove the container
docker rm postgres-db

# Remove everything and start fresh
docker stop postgres-db
docker rm postgres-db
docker volume prune  # Removes unused volumes

3. Configure environment variables:
Copy the `.env.example` file to `.env` and update the values according to your PostgreSQL setup.

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Testing

#Manual testing:

# Create an item
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Item","description":"Testing our FastAPI app"}'

# Get all items
curl "http://localhost:8000/items/"

# Get the item by ID (replace 1 with the ID from your create response)
curl "http://localhost:8000/items/1"

# Update the item
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Item","description":"This item has been updated"}'

# Delete the item
curl -X DELETE "http://localhost:8000/items/1"

#Automated testing:

# Run all tests
pytest -v

# Run only CRUD tests
pytest tests/test_crud.py

# Run a specific test
pytest tests/test_crud.py -k "test_partial_update_item"

## API Endpoints

- POST /items/ - Create a new item
- GET /items/ - Get all items
- GET /items/{item_id} - Get a specific item
- PUT /items/{item_id} - Update an item
- DELETE /items/{item_id} - Delete an item

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc