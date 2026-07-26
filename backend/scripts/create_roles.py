from app.core.database import SessionLocal
from app.models.role import Role


ROLES = [
    {
        "name": "USER",
        "description": "Regular application user",
    },
    {
        "name": "MODERATOR",
        "description": "Can moderate community content",
    },
    {
        "name": "ADMIN",
        "description": "Full administrative access",
    },
]


def create_roles():
    db = SessionLocal()

    try:
        for role_data in ROLES:

            existing_role = (
                db.query(Role)
                .filter(Role.name == role_data["name"])
                .first()
            )

            if existing_role:
                print(
                    f"Role already exists: {role_data['name']}"
                )
                continue

            role = Role(
                name=role_data["name"],
                description=role_data["description"],
            )

            db.add(role)

            print(
                f"Created role: {role_data['name']}"
            )

        db.commit()

        print("Roles creation completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    create_roles()