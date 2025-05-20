from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.oc_sort_item import OCSortItem


class OCOrder(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        # noinspection PyTypeChecker
        self.elements: List[OCSortItem] = elements

    def execute(self, context: Context) -> str:
        return ".order()" + self.elements[0].execute(context)

    async def async_execute(self, context: Context) -> str:
        return ".order()" + self.elements[0].execute(context)

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_OrderContext, supplier):
        return OCOrder(supplier(ctx))

    def __repr__(self):
        return ", ".join([str(e) for e in self.elements])
