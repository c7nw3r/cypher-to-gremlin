from typing import Tuple

from cypher_to_gremlin.__spi__.classes import CypherElementVisitor, CypherElement, Context
from cypher_to_gremlin.__spi__.types import Value
from cypher_to_gremlin.element.expression.oc_comparison_expression import OCComparisonExpression
from cypher_to_gremlin.element.expression.oc_list_predicate_expression import OCListPredicateExpression, get_source, \
    get_target
from cypher_to_gremlin.element.oc_property_lookup import OCPropertyLookup

ResolvableValue = Tuple[list[str], str, Value]


class ValuesVisitor(CypherElementVisitor, list[ResolvableValue]):
    def __init__(self, context: Context):
        super().__init__()
        self.context = context

    def visit(self, element: CypherElement):
        if isinstance(element, OCListPredicateExpression):
            source = get_source(element.elements[0], self.context)
            target = get_target(element.elements[1], self.context)

            if isinstance(target, OCPropertyLookup):
                self.append((
                    self.context.labels[element._resolve_variable()],
                    element._resolve_property(),
                    source
                ))

            else:
                self.append((
                    self.context.labels[element._resolve_variable()],
                    element._resolve_property(),
                    target
                ))

        if isinstance(element, OCComparisonExpression):
            _variable = element._resolve_variable()
            _property = element._resolve_property()
            _literals = element._resolve_literals()

            if isinstance(_literals, list):
                self.extend([
                    (self.context.labels[_variable], _property, e)
                    for e in _literals
                ])
            elif _literals is not None:
                self.append((self.context.labels[_variable], _property, _literals))
