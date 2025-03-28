from typing import List

from cypher_to_gremlin.__spi__.classes import (
    Context,
    CypherElement,
    CypherElementVisitor,
)
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.mixin.aggregate_mixin import AggregateMixin
from cypher_to_gremlin.mixin.variable_mixin import VariableVisitor


class OCReturn(CypherElement, AggregateMixin):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        visitor = VariableVisitor()
        self.accept(visitor)

        # order preserving deduplication
        var_names = list(dict.fromkeys(f'"{e}"' for e in visitor))

        if len(self.aggregators) > 0:
            # FIXME
            return f".count()"

        if len(var_names) > 0:
            return f".select({', '.join(var_names)})"

        return ""

    async def async_execute(self, context: Context) -> str:
        visitor = VariableVisitor()
        self.accept(visitor)

        # order preserving deduplication
        var_names = list(dict.fromkeys(f'"{e}"' for e in visitor))

        if len(self.aggregators) > 0:
            # FIXME
            return f".count()"

        if len(var_names) > 0:
            return f".select({', '.join(var_names)})"

        return ""

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_ReturnContext, supplier):
        return OCReturn(supplier(ctx))

    def __repr__(self):
        return f"RETURN {[''.join([str(e) for e in self.elements])]}"
