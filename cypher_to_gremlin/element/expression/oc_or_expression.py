from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, ExpressionContainer
from cypher_to_gremlin.__util__.async_util import gather_all
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCOrExpression(CypherElement, ExpressionContainer):

    def __init__(self, elements: List[CypherElement]):
        #if len(elements) == 1 and isinstance(elements[0], ExpressionContainer):
        #    self.elements = elements[0].get_expressions()
        #else:
        self.elements = elements

    def is_sufficient(self, context: Context):
        return all([e.is_sufficient(context) for e in self.elements])

    def execute(self, context: Context) -> str:
        return ".or(" + ", ".join([e.execute(context)[1:] for e in self.elements]) + ")"

    async def async_execute(self, context: Context) -> str:
        result = [e[1:] for e in await gather_all(self.elements, context)]
        return ".or(" + ", ".join(result) + ")"

    def get_expressions(self):
        return [self]

    @staticmethod
    def parse(ctx: CypherParser.OC_OrExpressionContext, supplier):
        elements = supplier(ctx)
        return OCOrExpression(elements) if len(elements) > 1 else elements

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return " OR ".join([str(e) for e in self.elements])
