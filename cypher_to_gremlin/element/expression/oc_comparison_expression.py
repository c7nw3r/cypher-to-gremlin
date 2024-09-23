from typing import List

from cypher_to_gremlin.__spi__.classes import Context, CypherElement
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCComparisonExpression(CypherElement):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    @property
    def var_name(self):
        # FIXME
        return self.elements[0].elements[0].name

    def execute(self, context: Context) -> str:
        return "".join(
            [
                e.execute(context.with_source(self.elements[0]))
                for e in self.elements[1:]
            ]
        )

    @staticmethod
    def parse(ctx: CypherParser.OC_ComparisonExpressionContext, supplier):
        return OCComparisonExpression(supplier(ctx))

    def is_sufficient(self, context: Context):
        try:
            return self.var_name in context.labels
        except Exception:
            return False

    def __repr__(self):
        return " ".join([str(e) for e in self.elements])
