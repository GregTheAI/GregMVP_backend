from sqlmodel import Session, create_engine, select, SQLModel

from app.core.config import settings
from app.dtos.CreateUser import UserCreate
from app.entities import User

engine = create_engine(str(settings.sqlalchemy_database_uri))


# make sure all SQLModel dtos are imported (app.dtos) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the dtos are already imported and registered from app.dtos
    SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        # user = crud.create_user(session=session, user_create=user_in)