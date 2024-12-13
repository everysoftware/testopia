import uuid
from typing import Any

import aiohttp
from aiohttp import BasicAuth


class AIAdapter:
    def __init__(
        self, gigachat_client_id: str, gigachat_client_secret: str
    ) -> None:
        self.gigachat_client_id = gigachat_client_id
        self.gigachat_client_secret = gigachat_client_secret
        self._token: str | None = None
        self._client: aiohttp.ClientSession | None = None

    @property
    def token(self) -> str:
        if self._token is None:
            raise Exception("Unauthorized")
        return self._token

    @property
    def client(self) -> aiohttp.ClientSession:
        if self._client is None:
            raise Exception("Please use async context manager")
        return self._client

    async def authorize(self) -> str:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4()),
        }
        payload = {"scope": "GIGACHAT_API_PERS"}
        auth = BasicAuth(self.gigachat_client_id, self.gigachat_client_secret)
        async with self.client.post(
            url=url, headers=headers, auth=auth, data=payload, ssl=False
        ) as response:
            token = await response.json()
            at = token["access_token"]
            self._token = at
            return at  # type: ignore[no-any-return]

    async def complete(self, text: str) -> str:
        payload = {
            "model": "GigaChat",
            "messages": [{"role": "user", "content": text}],
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        async with self.client.post(
            url=url, headers=headers, json=payload, ssl=False
        ) as response:
            data = await response.json()
            answer = data["choices"][0]["message"]["content"]
            return answer  # type: ignore[no-any-return]

    async def __aenter__(self) -> None:
        self._client = aiohttp.ClientSession()
        await self._client.__aenter__()
        await self.authorize()

    async def __aexit__(
        self, exc_type: Any, exc_val: Any, exc_tb: Any
    ) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)
        self._client = None
        self._token = None
