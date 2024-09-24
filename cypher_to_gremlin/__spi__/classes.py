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


class CypherElementVisitor:

    def visit(self, element: "CypherElement"):
        pass


class Visitable:

    def accept(self, visitor: CypherElementVisitor):
        pass


class CypherElement(ABC, Visitable):
    @abstractmethod
    def execute(self, context: Context) -> str:
        pass
