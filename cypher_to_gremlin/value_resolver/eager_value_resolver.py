from typing import Tuple, List

from cypher_to_gremlin.__spi__.protocols import ValueResolver
from cypher_to_gremlin.__spi__.types import Value
from cypher_to_gremlin.visitor.resolvable_value_visitor import ResolvableValue


# TODO: rename to LazyValueResolver
class EagerValueResolver(ValueResolver):
    def __init__(self, delegate: ValueResolver, resolvable_values: list[ResolvableValue]):
        self.delegate = delegate
        self.resolvable_values = resolvable_values
        self.cache = None

    def resolve(self, labels: List[str], key: str, value: Value) -> list[Value]:
        if self.cache is None:
            self.cache = {}
            result = self.batch_resolve(self.resolvable_values)
            for i, o in zip(self.resolvable_values, result):
                self.cache[str(i)] = o

        return self.cache[str((labels, key, value))]

    async def async_resolve(self, labels: List[str], key: str, value: Value) -> list[Value]:
        if self.cache is None:
            self.cache = {}
            result = await self.batch_async_resolve(self.resolvable_values)
            for i, o in zip(self.resolvable_values, result):
                self.cache[str(i)] = o

        return self.cache[str((labels, key, value))]

    def batch_resolve(self, values: list[Tuple[list[str], str, Value]]) -> list[list[Value]]:
        return self.delegate.batch_resolve(values)

    async def batch_async_resolve(self, values: list[Tuple[list[str], str, Value]]) -> list[list[Value]]:
        return await self.delegate.batch_async_resolve(values)
