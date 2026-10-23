import importlib
import asyncio
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


class LocalClient:
    def __init__(self, app):
        self.app = app

    def request(self, method: str, path: str, **kwargs):
        async def run():
            transport = httpx.ASGITransport(app=self.app)
            async with self.app.router.lifespan_context(self.app):
                async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                    return await client.request(method, path, **kwargs)
        return asyncio.run(run())

    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch):
    fixture = Path(__file__).parent / "fixtures" / "members.json"
    monkeypatch.setenv("AGRISOKO_DATA_PATH", str(fixture))
    import app.settings
    import app.main
    importlib.reload(app.settings)
    importlib.reload(app.main)
    yield LocalClient(app.main.app)

