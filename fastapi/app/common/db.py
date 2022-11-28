from .config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, Session

engine = create_engine('postgresql://{username}:{password}@{host}:{port}/{db_name}'.format(
    username=settings.DB_USER, password=settings.DB_PASSWORD, host=settings.DB_IP, port=settings.DB_PORT, db_name=settings.DB_NAME
), echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()


def get_db_session() -> Session:
    session: Session = db_session()
    return session