from asyncio import gather
from typing import Awaitable

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, StringLike, CharSequence, AsyncCharSequence


def gather_all(elements: list[CypherElement], context: Context) -> Awaitable[list[str, StringLike]]:
    return gather(*[e.async_execute(context) for e in elements])


async def completed(value: CharSequence) -> AsyncCharSequence:
    return value
