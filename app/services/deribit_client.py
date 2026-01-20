from dataclasses import dataclass
from typing import Any

import aiohttp


@dataclass(frozen=True)
class DeribitClient:
    base_url: str
    timeout_s: int = 10

    async def get_index_price(self, index_name: str) -> float:
        url = f"{self.base_url}/public/get_index_price"
        params = {"index_name": index_name}

        timeout = aiohttp.ClientTimeout(total=self.timeout_s)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=params) as resp:
                resp.raise_for_status()
                data: dict[str, Any] = await resp.json()

        result = data.get("result") or {}
        price = result.get("index_price")
        if price is None:
            raise ValueError(f"Unexpected response for {index_name}: {data}")
        return float(price)
