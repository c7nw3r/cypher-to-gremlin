from typing import List, Tuple

from cypher_to_gremlin.__spi__.protocols import ValueResolver
from cypher_to_gremlin.__spi__.types import Value


class DelegateValueResolver(ValueResolver):
    def __init__(self, callback):
        self.callback = callback

    def resolve(self, labels: List[str], key: str, value: Value) -> list[Value]:
        return self.callback(labels, key, value)

    async def async_resolve(self, labels: List[str], key: str, value: Value) -> list[Value]:
        return self.callback(labels, key, value)

    def batch_resolve(self, values: list[Tuple[list[str], str, Value]]) -> list[list[Value]]:
        return [
            self.callback(labels, key, value)
            for labels, key, value in values
        ]

    async def batch_async_resolve(self, values: list[Tuple[list[str], str, Value]]) -> list[list[Value]]:
        return [
            self.callback(labels, key, value)
            for labels, key, value in values
        ]