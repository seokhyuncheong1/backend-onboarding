from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base, Session

engine = create_engine('postgresql://{username}:{password}@{host}:{port}/{db_name}'.format(
    username='shcheong', password='shcheong', host='localhost', port='5432', db_name='test'
))
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


Base = declarative_base()


def get_db_session() -> Session:
    session: Session = db_session()
    return session