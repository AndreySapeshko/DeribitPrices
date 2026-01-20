import asyncio

from app.core.config import settings
from app.db.models import Base
from app.db.session import make_engine


async def init_models(conn):
    await conn.run_sync(Base.metadata.create_all)


# if __name__ == "__main__":
#     asyncio.run(init_models())
