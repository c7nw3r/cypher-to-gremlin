from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCWhere(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.expression = elements[0]

    def execute(self, context: Context) -> str:
        return self.expression.execute(context)

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        self.expression.accept(visitor)

    @staticmethod
    def parse(ctx: CypherParser.OC_WhereContext, supplier):
        return OCWhere(supplier(ctx))

    def __repr__(self):
        return f"WHERE {str(self.expression)}"
