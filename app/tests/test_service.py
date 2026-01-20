import pytest

from unittest.mock import AsyncMock

from app.services.price_service import PriceService


@pytest.mark.asyncio
async def test_fetch_and_store_price(session):
    mock_client = AsyncMock()
    mock_client.get_index_price.return_value = 12345.6789

    service = PriceService(client=mock_client)

    from app.db.repository import PriceRepository

    repo = PriceRepository(session)

    await service.fetch_and_store(repo, "btc_usd", "btc_usd")

    rows = await repo.get_all_by_ticker("btc_usd")

    assert len(rows) == 1
    assert float(rows[0].price) == 12345.6789
