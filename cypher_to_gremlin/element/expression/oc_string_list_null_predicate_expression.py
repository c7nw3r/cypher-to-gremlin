from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.oc_variable import OCVariable


class OCStringListNullPredicateExpression(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        elements = [e for e in self.elements if not isinstance(e, OCVariable)]
        return "".join([e.execute(context) for e in elements])

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_StringListNullPredicateExpressionContext, supplier):
        return OCStringListNullPredicateExpression(supplier(ctx))

    def __repr__(self):
        return "".join([str(e) for e in self.elements])
