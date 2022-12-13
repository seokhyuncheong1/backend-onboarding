from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session


db = SQLAlchemy()

def get_db_session() -> Session:
    return db.session
        