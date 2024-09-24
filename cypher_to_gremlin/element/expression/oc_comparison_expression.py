from typing import List

from cypher_to_gremlin.__spi__.classes import Context, CypherElement, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.mixin.var_name_mixin import VarNameMixin


class OCComparisonExpression(CypherElement, VarNameMixin):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        return "".join(
            [
                e.execute(context.with_source(self.elements[0]))
                for e in self.elements[1:]
            ]
        )

    @staticmethod
    def parse(ctx: CypherParser.OC_ComparisonExpressionContext, supplier):
        return OCComparisonExpression(supplier(ctx))

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return " ".join([str(e) for e in self.elements])
