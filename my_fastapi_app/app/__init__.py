"""
FastAPI CRUD Application package.
This package provides a RESTful API for managing items in a PostgreSQL database.
"""

from .config import settings
from .database import init_db, get_db
from .models import Item
from .schemas import ItemCreate, ItemUpdate, Item as ItemSchema