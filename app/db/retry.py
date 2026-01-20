import asyncio

from sqlalchemy import text
from sqlalchemy.exc import OperationalError


async def wait_for_db(conn, retries=10, delay=2):
    for i in range(retries):
        try:
            await conn.execute(text("SELECT 1"))
            return
        except OperationalError:
            await asyncio.sleep(delay)
    raise RuntimeError("Database not available")
