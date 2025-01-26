from sqlalchemy.orm import Session
from . import models, schemas
import logging

logger = logging.getLogger(__name__)

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())  # Changed from dict() to model_dump()
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        logger.info(f"Created item with id: {db_item.id}")
        return db_item
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        db.rollback()
        raise

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        update_data = item.model_dump(exclude_unset=True)  # Changed from dict() to model_dump()
        for key, value in update_data.items():
            setattr(db_item, key, value)
        try:
            db.commit()
            db.refresh(db_item)
            logger.info(f"Updated item with id: {item_id}")
            return db_item
        except Exception as e:
            logger.error(f"Error updating item: {e}")
            db.rollback()
            raise
    return None

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        try:
            db.delete(db_item)
            db.commit()
            logger.info(f"Deleted item with id: {item_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting item: {e}")
            db.rollback()
            raise
    return False