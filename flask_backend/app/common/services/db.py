from sqlalchemy.orm import Session

from app.common.db import get_db_session


class DBService:
    def __init__(self) -> None:
        self.db_session: Session = get_db_session()

    def __del__(self) -> None:
        print(">>>>>>>>>>>>>del called")
        self.db_session.commit()
        self.db_session.close()