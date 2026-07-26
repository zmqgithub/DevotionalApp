from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate


def get_roles(
    db: Session,
) -> list[Role]:

    return (
        db.query(Role)
        .order_by(Role.name)
        .all()
    )


def get_role(
    db: Session,
    role_id: int,
) -> Role:

    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )

    return role


def create_role(
    db: Session,
    data: RoleCreate,
) -> Role:

    existing_role = (
        db.query(Role)
        .filter(
            Role.name == data.name.upper()
        )
        .first()
    )

    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role already exists",
        )

    role = Role(
        name=data.name.upper(),
        description=data.description,
    )

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


def update_role(
    db: Session,
    role_id: int,
    data: RoleUpdate,
) -> Role:

    role = get_role(
        db,
        role_id,
    )

    if data.name is not None:

        existing_role = (
            db.query(Role)
            .filter(
                Role.name == data.name.upper(),
                Role.id != role_id,
            )
            .first()
        )

        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role already exists",
            )

        role.name = data.name.upper()

    if data.description is not None:
        role.description = data.description

    db.commit()
    db.refresh(role)

    return role


def delete_role(
    db: Session,
    role_id: int,
) -> None:

    role = get_role(
        db,
        role_id,
    )

    if role.name == "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ADMIN role cannot be deleted",
        )

    db.delete(role)
    db.commit()


def assign_role_to_user(
    db: Session,
    user_id: int,
    role_id: int,
) -> User:

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role = get_role(
        db,
        role_id,
    )

    if role not in user.roles:
        user.roles.append(role)

    db.commit()
    db.refresh(user)

    return user


def remove_role_from_user(
    db: Session,
    user_id: int,
    role_id: int,
) -> User:

    user = (
        db.query(User)
        .filter(
            User.id == user_id,
            User.is_deleted.is_(False),
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    role = get_role(
        db,
        role_id,
    )

    if role.name == "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ADMIN role cannot be removed",
        )

    if role in user.roles:
        user.roles.remove(role)

    db.commit()
    db.refresh(user)

    return user