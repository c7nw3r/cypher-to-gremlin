from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.mixin.var_name_mixin import VarNameMixin


class OCListPredicateExpression(CypherElement, VarNameMixin):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        return "".join(
            [
                e.execute(context.with_source(self.elements[0]))
                for e in self.elements[1:]
            ]
        )

    @staticmethod
    def parse(ctx: CypherParser.OC_ListPredicateExpressionContext, supplier):
        return OCListPredicateExpression(supplier(ctx))

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return f"IN {''.join([str(e) for e in self.elements])}"
