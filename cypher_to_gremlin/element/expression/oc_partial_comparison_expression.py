from cypher_to_gremlin.__spi__.classes import CypherElement, Context
from cypher_to_gremlin.__spi__.types import Operator
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.expression.oc_string_list_null_predicate_expression import \
    OCStringListNullPredicateExpression


class OCPartialComparisonExpression(CypherElement):

    def __init__(self, operator: Operator, value: CypherElement):
        self.operator = operator
        self.value = value

    def execute(self, context: Context) -> str:
        value = self.value.execute(context)

        _variable = self._resolve_variable(context)
        _property = self._resolve_property(context)

        # FIXME:
        value = context.value_resolver(context.labels[_variable], _property, value[1:-1])
        value = f'"{value}"'

        if self.operator == "=":
            return f'.has("{context.source.execute(context)}", {value})'
        raise ValueError(f"unknown expression operator '{self.operator}'")

    # noinspection PyMethodMayBeStatic
    def _resolve_variable(self, context: Context):
        if isinstance(context.source, OCStringListNullPredicateExpression):
            return context.source.elements[0].execute(context)
        raise ValueError("cannot resolve variable")

    # noinspection PyMethodMayBeStatic
    def _resolve_property(self, context: Context):
        if isinstance(context.source, OCStringListNullPredicateExpression):
            return context.source.elements[1].execute(context)
        raise ValueError("cannot resolve property")

    @staticmethod
    def parse(ctx: CypherParser.OC_PartialComparisonExpressionContext, supplier):
        segments = ctx.getText().split()
        elements = supplier(ctx)
        return OCPartialComparisonExpression(segments[0], elements[0])

    def __repr__(self):
        return f"{self.operator} {self.value.execute(Context())}"
