from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.__util__.list_util import find, opt_find
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.expression.oc_and_expression import OCAndExpression
from cypher_to_gremlin.element.oc_pattern import OCPattern
from cypher_to_gremlin.element.oc_where import OCWhere


class OCMatch(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements
        self.path = find(elements, OCPattern)

        where = opt_find(elements, OCWhere)
        if isinstance(where, OCWhere):
            self.expr = where.expression
        else:
            self.expr = None

    def execute(self, context: Context) -> str:
        if isinstance(self.expr, OCAndExpression):
            return self.path.execute(context.with_wheres(self.expr.get_expressions()))
        if self.expr:
            return self.path.execute(context.with_wheres([self.expr]))
        return self.path.execute(context)

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_MatchContext, supplier):
        return OCMatch(supplier(ctx))

    def __repr__(self):
        return f"MATCH {''.join([str(e) for e in self.elements])}"
