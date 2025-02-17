from abc import abstractmethod
from typing import Protocol, List, Union

from cypher_to_gremlin.__spi__.types import Value


class ValueResolver(Protocol):

    @abstractmethod
    def __call__(
        self, labels: List[str], key: str, value: Value | list[Value]
    ) -> Union[Value, List[Value]]:
        pass
