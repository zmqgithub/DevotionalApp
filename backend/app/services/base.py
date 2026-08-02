from typing import Generic, TypeVar, Type, Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.repositories.base import BaseRepository
from app.db.base_class import Base
from app.core.exceptions import (
    NotFoundError,
    ValidationError,
    DuplicateError,
    PermissionError
)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base service with common business logic
    """

    def __init__(self, repository: BaseRepository[ModelType, CreateSchemaType, UpdateSchemaType]):
        self.repository = repository

    def get_by_id(self, id: int) -> ModelType:
        """Get a record by ID"""
        record = self.repository.get_by_id(id)
        if not record:
            raise NotFoundError(f"{self.repository.model.__name__} with ID {id} not found")
        return record

    def get_all(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None,
            order_by: Optional[str] = None,
            order_desc: bool = False
    ) -> List[ModelType]:
        """Get all records with pagination"""
        return self.repository.get_all(
            skip=skip,
            limit=limit,
            filters=filters,
            order_by=order_by,
            order_desc=order_desc
        )

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records"""
        return self.repository.count(filters)

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record"""
        # Validate before creation
        self._validate_create(obj_in)

        # Check for duplicates
        self._check_duplicate_on_create(obj_in)

        return self.repository.create(obj_in)

    def create_bulk(self, objs_in: List[CreateSchemaType]) -> List[ModelType]:
        """Create multiple records"""
        for obj_in in objs_in:
            self._validate_create(obj_in)
            self._check_duplicate_on_create(obj_in)

        return self.repository.create_bulk(objs_in)

    def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> ModelType:
        """Update a record"""
        # Check if record exists
        existing = self.get_by_id(id)

        # Validate update
        self._validate_update(obj_in, existing)

        # Check for duplicates on update
        self._check_duplicate_on_update(obj_in, id)

        return self.repository.update(id, obj_in)

    def delete(self, id: int, soft_delete: bool = True) -> bool:
        """Delete a record"""
        # Check if record exists
        self.get_by_id(id)

        # Additional validation before delete
        self._validate_delete(id)

        return self.repository.delete(id, soft_delete)

    def exists(self, **kwargs) -> bool:
        """Check if a record exists"""
        return self.repository.exists(**kwargs)

    # Protected methods for overriding
    def _validate_create(self, obj_in: CreateSchemaType) -> None:
        """Validate before creation - override in child classes"""
        pass

    def _validate_update(self, obj_in: Union[UpdateSchemaType, Dict[str, Any]], existing: ModelType) -> None:
        """Validate before update - override in child classes"""
        pass

    def _validate_delete(self, id: int) -> None:
        """Validate before delete - override in child classes"""
        pass

    def _check_duplicate_on_create(self, obj_in: CreateSchemaType) -> None:
        """Check for duplicates on create - override in child classes"""
        pass

    def _check_duplicate_on_update(self, obj_in: Union[UpdateSchemaType, Dict[str, Any]], id: int) -> None:
        """Check for duplicates on update - override in child classes"""
        pass