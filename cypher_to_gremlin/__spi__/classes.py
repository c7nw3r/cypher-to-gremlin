from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Literal, Optional

from cypher_to_gremlin.__spi__.protocols import ValueResolver

Dialect = Literal["tinkerpop", "gremlinpython"]


@dataclass
class Context:
    source: Optional["CypherElement"] = None
    labels: dict = field(default_factory=lambda: {})
    wheres: List["CypherElement"] = field(default_factory=lambda: [])
    value_resolver: ValueResolver = lambda *e: e[2]
    dialect: Dialect = "tinkerpop"

    def with_source(self, source: Optional["CypherElement"]):
        return Context(
            source, self.labels, self.wheres, self.value_resolver, self.dialect
        )

    def with_wheres(self, wheres: List["CypherElement"]):
        return Context(
            self.source, self.labels, [*wheres], self.value_resolver, self.dialect
        )


class CypherElement(ABC):
    @abstractmethod
    def execute(self, context: Context) -> str:
        pass

    # TODO: find better / correct solution
    # recursive evaluation of var name for first element
    @property
    def var_name(self) -> str:
        try:
            return self.elements[0].var_name
        except Exception:
            return ""
