from app.common.db import async_db_session


class AsyncDBService:
    def __init__(self):
        self.db_session = async_db_session

    async def __aenter__(self):
        print(">>>>>>>>>>>>aenter called")
        return self

    async def __aexit__(self, *args):
        print(">>>>>>>>>>>>aexit called")
        await self.db_session.commit()
        await self.db_session.remove()
        return self