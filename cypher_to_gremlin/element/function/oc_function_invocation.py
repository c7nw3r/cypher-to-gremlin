from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCFunctionInvocation(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    @property
    def name(self):
        return self.elements[0].name

    def execute(self, context: Context) -> str:
        return f"{self.elements[0]}({''.join([str(e) for e in self.elements[1:]])})"

    @staticmethod
    def parse(ctx: CypherParser.OC_FunctionInvocationContext, supplier):
        return OCFunctionInvocation(supplier(ctx))

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return f"{self.elements[0]}({''.join([str(e) for e in self.elements[1:]])})"
