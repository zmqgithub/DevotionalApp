from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.user import User


def create_superadmin():
    db: Session = SessionLocal()

    email = "admin@devotionalapp.com"
    password = "Admin@12345"

    try:
        existing_user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if existing_user:
            print(f"User already exists: {email}")
            return

        admin = User(
            name="Super Admin",
            email=email,
            password_hash=hash_password(password),
            is_active=True,
            is_deleted=False,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Super admin created successfully!")
        print(f"ID: {admin.id}")
        print(f"Email: {email}")
        print(f"Password: {password}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_superadmin()