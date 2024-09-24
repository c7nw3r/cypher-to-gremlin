from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.__spi__.types import Operator, Value
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCStringListNullPredicateExpression(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        return self.elements[-1].execute(context)

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_StringListNullPredicateExpressionContext, supplier):
        return OCStringListNullPredicateExpression(supplier(ctx))

    def __repr__(self):
        return "".join([str(e) for e in self.elements])
