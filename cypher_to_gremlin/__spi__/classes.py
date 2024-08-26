from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, List

from cypher_to_gremlin.__spi__.protocols import ValueResolver


@dataclass
class Context:
    source: Optional['CypherElement'] = None
    labels: dict = field(default_factory=lambda: {})
    wheres: List['CypherElement'] = field(default_factory=lambda: [])
    value_resolver: ValueResolver = lambda *e: e[2]
    as_code: bool = False

    def with_source(self, source: Optional['CypherElement']):
        return Context(source, self.labels, self.wheres, self.value_resolver)

    def with_wheres(self, wheres: List['CypherElement']):
        return Context(self.source, self.labels, [*wheres], self.value_resolver)


class CypherElement(ABC):

    @abstractmethod
    def execute(self, context: Context) -> str:
        pass
