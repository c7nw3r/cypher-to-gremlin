from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.mixin.property_mixin import PropertyVisitor


class OCSortItem(CypherElement):

    def __init__(self, elements: List[CypherElement], descending: bool):
        # noinspection PyTypeChecker
        self.elements: List[CypherElement] = elements
        self.descending = descending

    @property
    def property_name(self) -> str:
        visitor = PropertyVisitor()
        self.accept(visitor)
        return visitor[0]

    def execute(self, context: Context) -> str:
        return f'.by("{self.property_name}", {"desc" if self.descending else "asc"})'

    async def async_execute(self, context: Context) -> str:
        return f'.by("{self.property_name}", {"desc" if self.descending else "asc"})'

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_SortItemContext, supplier):
        descending = "desc" in ctx.getText().lower()
        return OCSortItem(supplier(ctx), descending)

    def __repr__(self):
        return ", ".join([str(e) for e in self.elements])
