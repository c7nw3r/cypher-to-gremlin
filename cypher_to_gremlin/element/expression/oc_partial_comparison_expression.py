from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, CharSequence, \
    AsyncCharSequence
from cypher_to_gremlin.__spi__.types import Operator
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCPartialComparisonExpression(CypherElement):

    def __init__(self, operator: Operator, elements: List[CypherElement]):
        self.operator = operator
        self.elements = elements

    def execute(self, context: Context, **kwargs) -> CharSequence:
        return self.operator

    async def async_execute(self, context: Context, **kwargs) -> AsyncCharSequence:
        return self.operator

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_PartialComparisonExpressionContext, supplier):
        segments = ctx.getText().split()
        return OCPartialComparisonExpression(segments[0], supplier(ctx))

    def __repr__(self):
        return f"{self.operator} {self.elements}"
