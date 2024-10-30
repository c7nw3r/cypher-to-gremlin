from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Literal, Union

from cypher_to_gremlin.__spi__.protocols import ValueResolver

Dialect = Literal["tinkerpop", "gremlinpython"]


@dataclass
class Context:
    labels: dict = field(default_factory=lambda: {})
    wheres: List["CypherElement"] = field(default_factory=lambda: [])
    value_resolver: ValueResolver = lambda *e: e[2]
    dialect: Dialect = "tinkerpop"
    alias: bool = True

    def with_wheres(self, wheres: List["CypherElement"]):
        return Context(
            self.labels, [*wheres], self.value_resolver, self.dialect, self.alias
        )

    def with_alias(self, alias: bool):
        return Context(
            self.labels, self.wheres, self.value_resolver, self.dialect, alias
        )


class CypherElementVisitor:

    def visit(self, element: "CypherElement"):
        pass


class Visitable:

    def accept(self, visitor: CypherElementVisitor):
        pass


class StringLike:
    def __init__(self, segments: List[str]):
        self.segments = segments

    def __getitem__(self, item):
        return self.segments[item]

    def __str__(self):
        return "".join(self.segments)


CharSequence = Union[str, StringLike]


class CypherElement(ABC, Visitable):
    @abstractmethod
    def execute(self, context: Context) -> CharSequence:
        pass
