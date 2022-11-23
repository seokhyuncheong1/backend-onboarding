from app import create_app
from app.routers import api_router

app = create_app()
app.include_router(api_router, prefix="/api")