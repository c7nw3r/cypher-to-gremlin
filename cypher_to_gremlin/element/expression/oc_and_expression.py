from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCAndExpression(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        return "".join([e.execute(context) for e in self.elements])

    @staticmethod
    def parse(ctx: CypherParser.OC_AndExpressionContext, supplier):
        return OCAndExpression(supplier(ctx))

    def __repr__(self):
        return " AND ".join([str(e) for e in self.elements])
