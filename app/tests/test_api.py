import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.api.main import app
from app.api.routes import get_session


@pytest.mark.asyncio
async def test_get_prices_requires_ticker():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/prices")

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_prices(session, engine):
    sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)

    async def override_get_session():
        async with sessionmaker() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    from app.db.repository import PriceRepository

    repo = PriceRepository(session)
    await repo.add_tick("btc_usd", 100, 1)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/prices", params={"ticker": "btc_usd"})

        assert response.status_code == 200
        data = response.json()

    assert len(data) == 1
    assert data[0]["ticker"] == "btc_usd"
