from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Literal, Union, Awaitable

from cypher_to_gremlin.__spi__.protocols import ValueResolver, NoOpValueResolver

Dialect = Literal["tinkerpop", "gremlinpython"]


@dataclass
class Context:
    labels: dict = field(default_factory=lambda: {})
    wheres: List["CypherElement"] = field(default_factory=lambda: [])
    value_resolver: ValueResolver = field(default_factory=lambda: NoOpValueResolver())
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

    def with_labels(self, labels: dict):
        return Context(
            labels, self.wheres, self.value_resolver, self.dialect, self.alias
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
AsyncCharSequence = Awaitable[str | StringLike]


class CypherElement(ABC, Visitable):
    @abstractmethod
    def execute(self, context: Context) -> CharSequence:
        pass

    @abstractmethod
    async def async_execute(self, context: Context) -> AsyncCharSequence:
        pass


class ExpressionContainer(ABC):

    @abstractmethod
    def get_expressions(self) -> List[CypherElement]:
        pass
