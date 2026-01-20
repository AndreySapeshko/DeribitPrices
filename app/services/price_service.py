import time
from dataclasses import dataclass

from app.db.repository import PriceRepository
from app.services.deribit_client import DeribitClient


@dataclass
class PriceService:
    client: DeribitClient

    async def fetch_and_store(self, repo: PriceRepository, ticker: str, index_name: str) -> None:
        price = await self.client.get_index_price(index_name=index_name)
        ts_unix = int(time.time())
        await repo.add_tick(ticker=ticker, price=price, ts_unix=ts_unix)
