from abc import abstractmethod
from typing import Protocol, List, Tuple

from cypher_to_gremlin.__spi__.types import Value


class ValueResolver(Protocol):

    @abstractmethod
    def resolve(self, labels: List[str], key: str, value: Value) -> list[Value]:
        pass

    @abstractmethod
    async def async_resolve(self, labels: List[str], key: str, value: Value) -> list[Value]:
        pass

    @abstractmethod
    def batch_resolve(self, values: list[Tuple[list[str], str, Value]]) -> list[list[Value]]:
        pass

    @abstractmethod
    async def batch_async_resolve(self, values: list[Tuple[list[str], str, Value]]) -> list[list[Value]]:
        pass


class NoOpValueResolver(ValueResolver):

    def resolve(self, labels: List[str], key: str, value: Value) -> list[Value]:
        return value if isinstance(value, list) else [value]

    async def async_resolve(self, labels: List[str], key: str, value: Value) -> list[Value]:
        return value if isinstance(value, list) else [value]

    def batch_resolve(self, values: list[Tuple[list[str], str, Value]]) -> list[list[Value]]:
        return [[e[2]] for e in values]

    async def batch_async_resolve(self, values: list[Tuple[list[str], str, Value]]) -> list[list[Value]]:
        return [[e[2]] for e in values]


