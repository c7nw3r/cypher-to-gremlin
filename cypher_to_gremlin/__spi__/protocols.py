from abc import abstractmethod
from typing import Protocol, List, Union

from cypher_to_gremlin.__spi__.types import Value


class ValueResolver(Protocol):

    @abstractmethod
    def __call__(self, labels: List[str], key: str, value: Value) -> Union[Value, List[Value]]:
        pass

    async def async_resolve(self, labels: List[str], key: str, value: Value) -> Union[Value, List[Value]]:
        pass


class NoOpValueResolver(ValueResolver):
    def __init__(self, as_list: bool = False):
        self.as_list = as_list

    def __call__(self, labels: List[str], key: str, value: Value) -> Union[Value, List[Value]]:
        return value if not self.as_list else [value]
