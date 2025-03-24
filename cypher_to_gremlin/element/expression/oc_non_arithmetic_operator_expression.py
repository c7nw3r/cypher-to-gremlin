from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.__util__.async_util import gather_all
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCNonArithmeticOperatorExpression(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        return "".join([e.execute(context) for e in self.elements])

    async def async_execute(self, context: Context) -> str:
        return "".join(await gather_all(self.elements, context))

    @staticmethod
    def parse(ctx: CypherParser.OC_NonArithmeticOperatorExpressionContext, supplier):
        elements = supplier(ctx)
        return OCNonArithmeticOperatorExpression(elements) if len(elements) > 1 else elements

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return " ".join([str(e) for e in self.elements])
