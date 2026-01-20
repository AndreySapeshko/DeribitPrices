from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import PriceTick


class PriceRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_tick(self, ticker: str, price: float, ts_unix: int) -> PriceTick:
        tick = PriceTick(ticker=ticker, price=price, ts_unix=ts_unix)
        self._session.add(tick)
        await self._session.commit()
        return tick

    async def get_all_by_ticker(self, ticker: str) -> list[PriceTick]:
        q = select(PriceTick).where(PriceTick.ticker == ticker).order_by(PriceTick.ts_unix.asc())
        res = await self._session.execute(q)
        return list(res.scalars().all())

    async def get_last_by_ticker(self, ticker: str) -> PriceTick | None:
        q = select(PriceTick).where(PriceTick.ticker == ticker).order_by(desc(PriceTick.ts_unix)).limit(1)
        res = await self._session.execute(q)
        return res.scalars().first()

    async def get_by_ticker_and_ts_range(self, ticker: str, ts_from: int | None, ts_to: int | None) -> list[PriceTick]:
        q = select(PriceTick).where(PriceTick.ticker == ticker)
        if ts_from is not None:
            q = q.where(PriceTick.ts_unix >= ts_from)
        if ts_to is not None:
            q = q.where(PriceTick.ts_unix <= ts_to)
        q = q.order_by(PriceTick.ts_unix.asc())
        res = await self._session.execute(q)
        return list(res.scalars().all())
