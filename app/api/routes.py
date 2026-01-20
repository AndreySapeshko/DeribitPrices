from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.repository import PriceRepository
from app.db.session import make_engine, make_session_factory

router = APIRouter()

_engine = make_engine(settings.database_url)
_session_factory = make_session_factory(_engine)


async def get_session() -> AsyncSession:
    async with _session_factory() as session:
        yield session


@router.get("/prices")
async def get_prices(
    ticker: str = Query(...),
    session: AsyncSession = Depends(get_session),
):
    repo = PriceRepository(session)
    rows = await repo.get_all_by_ticker(ticker)
    return [{"ticker": r.ticker, "price": float(r.price), "ts_unix": r.ts_unix} for r in rows]


@router.get("/prices/last")
async def get_last_price(
    ticker: str = Query(...),
    session: AsyncSession = Depends(get_session),
):
    repo = PriceRepository(session)
    last = await repo.get_last_by_ticker(ticker)
    if not last:
        raise HTTPException(status_code=404, detail="No data for ticker")
    return {"ticker": last.ticker, "price": float(last.price), "ts_unix": last.ts_unix}


@router.get("/prices/range")
async def get_prices_by_date(
    ticker: str = Query(...),
    ts_from: int | None = Query(None, description="Unix timestamp from"),
    ts_to: int | None = Query(None, description="Unix timestamp to"),
    session: AsyncSession = Depends(get_session),
):
    repo = PriceRepository(session)
    rows = await repo.get_by_ticker_and_ts_range(ticker, ts_from, ts_to)
    return [{"ticker": r.ticker, "price": float(r.price), "ts_unix": r.ts_unix} for r in rows]
