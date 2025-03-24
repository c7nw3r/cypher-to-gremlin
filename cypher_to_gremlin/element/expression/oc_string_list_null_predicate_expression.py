from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, AsyncCharSequence, \
    CharSequence
from cypher_to_gremlin.__util__.async_util import gather_all
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.expression.oc_comparison_expression import OCComparisonExpression
from cypher_to_gremlin.element.expression.oc_list_predicate_expression import OCListPredicateExpression
from cypher_to_gremlin.element.oc_variable import OCVariable
from cypher_to_gremlin.mixin.variable_mixin import VariableMixin


class OCStringListNullPredicateExpression(CypherElement, VariableMixin):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> CharSequence:
        elements = [e for e in self.elements if not isinstance(e, OCVariable)]
        return "".join([e.execute(context) for e in elements])

    async def async_execute(self, context: Context) -> AsyncCharSequence:
        elements = [e for e in self.elements if not isinstance(e, OCVariable)]
        return "".join(await gather_all(elements, context))

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_StringListNullPredicateExpressionContext, supplier):
        elements = supplier(ctx)
        if len(elements) == 1:
            return elements

        if "NULL" in ctx.getText().upper():
            return OCComparisonExpression(elements)

        return OCListPredicateExpression(elements)

    def __repr__(self):
        return "".join([str(e) for e in self.elements])
