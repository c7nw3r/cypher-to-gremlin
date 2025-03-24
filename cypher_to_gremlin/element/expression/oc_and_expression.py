from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, ExpressionContainer
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCAndExpression(CypherElement, ExpressionContainer):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        return "".join([e.execute(context) for e in self.elements])

    async def async_execute(self, context: Context) -> str:
        return "".join([await e.async_execute(context) for e in self.elements])

    def is_sufficient(self, context: Context):
        return all([e.is_sufficient(context) for e in self.elements])

    def get_expressions(self):
        expressions = [e.get_expressions() if isinstance(e, ExpressionContainer) else [e] for e in self.elements]
        return [e for sublist in expressions for e in sublist]

    @staticmethod
    def parse(ctx: CypherParser.OC_AndExpressionContext, supplier):
        elements = supplier(ctx)
        return OCAndExpression(elements) if len(elements) > 1 else elements

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return " AND ".join([str(e) for e in self.elements])
