from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCLimit(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.literal = elements[0]

    def execute(self, context: Context) -> str:
        return f".limit({self.literal})"

    async def async_execute(self, context: Context) -> str:
        return f".limit({self.literal})"

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(ctx: CypherParser.OC_LimitContext, supplier):
        return OCLimit(supplier(ctx))

    def __repr__(self):
        return f"LIMIT {self.literal}"
