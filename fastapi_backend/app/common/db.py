from .config import settings

from asyncio import current_task
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, Session
from sqlalchemy.ext.asyncio import create_async_engine, async_scoped_session, AsyncSession

engine = create_engine('postgresql://{username}:{password}@{host}:{port}/{db_name}'.format(
    username=settings.DB_USER, password=settings.DB_PASSWORD, host=settings.DB_IP, port=settings.DB_PORT, db_name=settings.DB_NAME
), echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

async_engine = create_async_engine('postgresql+asyncpg://{username}:{password}@{host}:{port}/{db_name}'.format(
    username=settings.DB_USER, password=settings.DB_PASSWORD, host=settings.DB_IP, port=settings.DB_PORT, db_name=settings.DB_NAME
), echo=True)
async_session_factory = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=async_engine, class_=AsyncSession)
async_db_session = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=current_task
)


Base = declarative_base()


def get_db_session() -> Session:
    session: Session = db_session()
    return session
