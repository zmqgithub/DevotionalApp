from app.core.database import SessionLocal
from app.models.user import User
from app.models.role import Role


ADMIN_EMAIL = "admin@devotionalapp.com"
ADMIN_ROLE_NAME = "ADMIN"


def assign_admin_role():
    db = SessionLocal()

    try:
        # Find the admin user
        user = (
            db.query(User)
            .filter(
                User.email == ADMIN_EMAIL,
                User.is_deleted.is_(False),
            )
            .first()
        )

        if not user:
            print(
                f"User not found: {ADMIN_EMAIL}"
            )
            return

        # Find the ADMIN role
        admin_role = (
            db.query(Role)
            .filter(
                Role.name == ADMIN_ROLE_NAME
            )
            .first()
        )

        if not admin_role:
            print(
                f"Role not found: {ADMIN_ROLE_NAME}"
            )
            print(
                "Run 'python -m scripts.create_roles' first."
            )
            return

        # Check if the user already has ADMIN role
        if admin_role in user.roles:
            print(
                f"User {ADMIN_EMAIL} already has "
                f"the {ADMIN_ROLE_NAME} role."
            )
            return

        # Assign ADMIN role
        user.roles.append(admin_role)

        db.commit()

        print(
            f"Successfully assigned {ADMIN_ROLE_NAME} "
            f"role to {ADMIN_EMAIL}"
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    assign_admin_role()