from app import create_app
from app.routers import api_router
from app.middlewares.auth_middleware import LoginCheckMiddleware


app = create_app()
app.include_router(api_router, prefix="/api")
app.add_middleware(LoginCheckMiddleware)