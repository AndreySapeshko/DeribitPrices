from fastapi import FastAPI

from app.core.config import settings
from app.db.init_db import init_models
from app.db.retry import wait_for_db
from app.db.session import make_engine

# from app.api.routes import router

app = FastAPI(title="Deribit Prices API")
# app.include_router(router)


@app.on_event("startup")
async def on_startup():
    engine = make_engine(settings.database_url)
    async with engine.begin() as conn:
        await wait_for_db(conn)
        await init_models(conn)
    await engine.dispose()
