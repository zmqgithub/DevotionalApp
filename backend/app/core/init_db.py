from app.db.session import Base, engine
from app.modules.users.model import  User


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")