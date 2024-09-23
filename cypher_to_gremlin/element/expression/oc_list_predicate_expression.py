from typing import List

from mygpt.graph.cypher_to_gremlin.__spi__.classes import Context, CypherElement
from mygpt.graph.cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCListPredicateExpression(CypherElement):
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
    def parse(ctx: CypherParser.OC_ListPredicateExpressionContext, supplier):
        return OCListPredicateExpression(supplier(ctx))

    def is_sufficient(self, context: Context):
        try:
            return self.var_name in context.labels
        except Exception:
            return False

    def __repr__(self):
        return f"IN {"".join([str(e) for e in self.elements])}"
