import asyncio

from app.core.config import settings
from app.db.repository import PriceRepository
from app.db.session import make_engine, make_session_factory
from app.services.deribit_client import DeribitClient
from app.services.price_service import PriceService
from app.workers.celery_app import celery_app

TICKERS = {
    "btc_usd": "btc_usd",
    "eth_usd": "eth_usd",
}


async def _run() -> None:
    engine = make_engine(settings.database_url)
    session_factory = make_session_factory(engine)

    client = DeribitClient(base_url=settings.DERIBIT_BASE_URL)
    service = PriceService(client=client)

    async with session_factory() as session:
        repo = PriceRepository(session)
        for ticker, index_name in TICKERS.items():
            price = await service.fetch_and_store(repo=repo, ticker=ticker, index_name=index_name)
            print(price)

    await engine.dispose()


@celery_app.task(name="app.workers.tasks.fetch_prices")
def fetch_prices() -> None:
    asyncio.run(_run())


if __name__ == "__main__":
    asyncio.run(_run())
