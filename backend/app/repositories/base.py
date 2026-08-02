from typing import Generic, TypeVar, Type, Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session, Query
from sqlalchemy import func, and_, or_
from pydantic import BaseModel
from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base repository with CRUD operations
    """

    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model

    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            order_desc: bool = False
    ) -> List[ModelType]:
        """Get all records with pagination and filtering"""
        query = self.db.query(self.model)

        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.filter(getattr(self.model, key) == value)

        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            order_column = getattr(self.model, order_by)
            query = query.order_by(order_column.desc() if order_desc else order_column)

        # Apply pagination
        return query.offset(skip).limit(limit).all()

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filters"""
        query = self.db.query(func.count(self.model.id))

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.filter(getattr(self.model, key) == value)

        return query.scalar() or 0

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def create_bulk(self, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        """Create multiple records"""
        db_objs = []
        for obj_in in objs_in:
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            db_objs.append(db_obj)

        self.db.add_all(db_objs)
        self.db.commit()

        # Refresh all objects
        for db_obj in db_objs:
            self.db.refresh(db_obj)

        return db_objs

    def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> Optional[ModelType]:
        """Update a record"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return None

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int, soft_delete: bool = True) -> bool:
        """Delete a record (soft delete by default)"""
        db_obj = self.get_by_id(id)
        if not db_obj:
            return False

        if soft_delete and hasattr(db_obj, 'is_active'):
            db_obj.is_active = False
            self.db.commit()
        else:
            self.db.delete(db_obj)
            self.db.commit()

        return True

    def delete_permanent(self, id: int) -> bool:
        """Permanently delete a record"""
        return self.delete(id, soft_delete=False)

    def exists(self, **kwargs) -> bool:
        """Check if a record exists with given filters"""
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)
        return query.first() is not None

    def get_or_create(self, defaults: Optional[Dict[str, Any]] = None, **kwargs) -> tuple[ModelType, bool]:
        """Get a record or create it if it doesn't exist"""
        query = self.db.query(self.model)
        for key, value in kwargs.items():
            if hasattr(self.model, key):
                query = query.filter(getattr(self.model, key) == value)

        instance = query.first()
        if instance:
            return instance, False

        # Create new instance
        params = {**kwargs}
        if defaults:
            params.update(defaults)

        db_obj = self.model(**params)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj, True

    def bulk_update(self, ids: List[int], update_data: Dict[str, Any]) -> int:
        """Bulk update records"""
        if not ids:
            return 0

        query = self.db.query(self.model).filter(self.model.id.in_(ids))
        count = query.update(update_data, synchronize_session=False)
        self.db.commit()
        return count