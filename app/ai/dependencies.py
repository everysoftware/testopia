from typing import Annotated, AsyncIterator

from fast_depends import Depends

from app.ai.adapter import AIAdapter
from app.ai.config import ai_settings

ai = AIAdapter(
    ai_settings.gigachat_client_id, ai_settings.gigachat_client_secret
)


async def get_ai() -> AsyncIterator[AIAdapter]:
    async with ai:
        yield ai


AIDep = Annotated[AIAdapter, Depends(get_ai)]
