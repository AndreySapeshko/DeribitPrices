import time

import pytest

from app.db.repository import PriceRepository


@pytest.mark.asyncio
async def test_add_and_get_price(session):
    repo = PriceRepository(session)

    ts = int(time.time())
    await repo.add_tick("btc_usd", 30000.123456, ts)

    rows = await repo.get_all_by_ticker("btc_usd")

    assert len(rows) == 1
    assert rows[0].ticker == "btc_usd"
    assert float(rows[0].price) == 30000.123456
    assert rows[0].ts_unix == ts


@pytest.mark.asyncio
async def test_get_last_price(session):
    repo = PriceRepository(session)

    await repo.add_tick("eth_usd", 1000, 1)
    await repo.add_tick("eth_usd", 2000, 2)

    last = await repo.get_last_by_ticker("eth_usd")

    assert float(last.price) == 2000
    assert last.ts_unix == 2
