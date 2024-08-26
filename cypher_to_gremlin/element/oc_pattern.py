from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCPattern(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        return "".join([e.execute(context) for e in self.elements])

    @staticmethod
    def parse(ctx: CypherParser.OC_PatternContext, supplier):
        return OCPattern(supplier(ctx))

    def __repr__(self):
        return "".join([str(e) for e in self.elements])
