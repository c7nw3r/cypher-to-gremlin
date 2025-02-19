from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.__util__.str_util import decorate_literal
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.oc_literal import OCLiteral
from cypher_to_gremlin.element.oc_property_lookup import OCPropertyLookup
from cypher_to_gremlin.mixin.property_mixin import PropertyVisitor
from cypher_to_gremlin.mixin.variable_mixin import VariableMixin, VariableVisitor


def get_source(element: CypherElement, context: Context):
    if isinstance(element, OCLiteral):
        return element.execute(context).replace("'", '').replace('"', '')

    visitor = PropertyVisitor()
    element.accept(visitor)

    return visitor[0]


def get_target(element: CypherElement, context: Context):
    collector = []

    class TargetVisitor(CypherElementVisitor):
        def visit(self, element: "CypherElement"):
            if isinstance(element, OCLiteral):
                collector.append(element.execute(context))

            if isinstance(element, OCPropertyLookup):
                collector.append(element)

    element.accept(TargetVisitor())

    if len(collector) == 1 and isinstance(collector[0], OCPropertyLookup):
        return collector[0]
    return collector


class OCListPredicateExpression(CypherElement, VariableMixin):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        source = get_source(self.elements[0], context)
        target = get_target(self.elements[1], context)

        if isinstance(target, OCPropertyLookup):
            _variable = self._resolve_variable()
            _property = self._resolve_property()
            source = context.value_resolver(
                context.labels[_variable], _property, source
            )

            if isinstance(source, list):
                source = ", ".join([decorate_literal(e) for e in source])
                if context.dialect == "gremlinpython":
                    return f'.has("{target.name}", within([{source}]))'
                return f'.has("{target.name}", within({source}))'

            return f'.has("{target.name}", {decorate_literal(source)})'

        _variable = self._resolve_variable()
        _property = self._resolve_property()
        target = context.value_resolver(
            context.labels[_variable], _property, target
        )

        if isinstance(target, list):
            target = ", ".join([decorate_literal(e) for e in target])
            if context.dialect == "gremlinpython":
                return f'.has("{source}", within([{target}]))'
            return f'.has("{source}", within({target}))'

        return f'.has("{source}", {decorate_literal(target)})'

    def _resolve_variable(self):
        visitor = VariableVisitor()
        [e.accept(visitor) for e in self.elements]
        return visitor[0] if len(visitor) > 0 else None

    def _resolve_property(self):
        visitor = PropertyVisitor()
        [e.accept(visitor) for e in self.elements]
        return visitor[0] if len(visitor) > 0 else None

    @staticmethod
    def parse(ctx: CypherParser.OC_ListPredicateExpressionContext, supplier):
        elements = supplier(ctx)
        return OCListPredicateExpression(elements)

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return f"IN {''.join([str(e) for e in self.elements])}"
