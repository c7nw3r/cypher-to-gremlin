from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context
from cypher_to_gremlin.__spi__.types import Operator, Value
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCStringListNullPredicateExpression(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        return self.elements[-1].execute(context)

    @staticmethod
    def parse(ctx: CypherParser.OC_StringListNullPredicateExpressionContext, supplier):
        return OCStringListNullPredicateExpression(supplier(ctx))

    def __repr__(self):
        return "".join([str(e) for e in self.elements])
