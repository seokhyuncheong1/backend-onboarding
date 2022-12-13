from flask import Flask

from app.common.config import Config
from app.routers import api
from app.common.db import db


def create_app() -> Flask:
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    api.init_app(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
