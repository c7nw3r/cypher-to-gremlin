from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.__util__.list_util import flatten
from cypher_to_gremlin.__util__.str_util import decorate_literal
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.oc_literal import OCLiteral
from cypher_to_gremlin.element.oc_property_lookup import OCPropertyLookup
from cypher_to_gremlin.mixin.property_mixin import PropertyVisitor
from cypher_to_gremlin.mixin.variable_mixin import VariableMixin, VariableVisitor

SKIP_VALUE_RESOLVER = ["startingWith", "endingWith"]

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


def render_property(source, target, context, predicate: str) -> str:
    if len(source) == 1:
        source = source[0]

    if isinstance(source, list):
        source = ", ".join([decorate_literal(e) for e in source])
        if context.dialect == "gremlinpython":
            return f'.has("{target.name}", {predicate}([{source}]))'
        if context.dialect == "cosmosdb":
            return f'.has("{target.name}", {predicate}([{source}]))'
        return f'.has("{target.name}", {predicate}({source}))'

    return f'.has("{target.name}", {decorate_literal(source)})'

def render_list(source, target, context, predicate: str) -> str:
    if len(source) == 1:
        source = source[0]

    if predicate in SKIP_VALUE_RESOLVER:
        return f'.has("{source}", {predicate}({decorate_literal(target[0])}))'

    if isinstance(target, list):
        target = ", ".join([decorate_literal(e) for e in target])
        if context.dialect == "gremlinpython":
            return f'.has("{source}", {predicate}([{target}]))'
        if context.dialect == "cosmosdb":
            return f'.has("{source}", {predicate}([{target}]))'
        return f'.has("{source}", {predicate}({target}))'

    return f'.has("{source}", {decorate_literal(target)})'


class OCListPredicateExpression(CypherElement, VariableMixin):
    def __init__(self, elements: List[CypherElement], predicate: str):
        self.elements = elements
        self.predicate = predicate

    def execute(self, context: Context) -> str:
        source = get_source(self.elements[0], context)
        target = get_target(self.elements[1], context)

        if isinstance(target, OCPropertyLookup):
            source = context.value_resolver.resolve(
                labels=context.labels[self._resolve_variable()],
                key=self._resolve_property(),
                value=source
            ) if self.predicate not in SKIP_VALUE_RESOLVER else source
            return render_property(source, target, context, self.predicate)

        target = [context.value_resolver.resolve(
            labels=context.labels[self._resolve_variable()],
            key=self._resolve_property(),
            value=e
        ) for e in target] if self.predicate not in SKIP_VALUE_RESOLVER else [target]
        target = flatten(target)
        return render_list(source, target, context, self.predicate)

    async def async_execute(self, context: Context) -> str:
        source = get_source(self.elements[0], context)
        target = get_target(self.elements[1], context)

        if isinstance(target, OCPropertyLookup):
            source = await context.value_resolver.async_resolve(
                labels=context.labels[self._resolve_variable()],
                key=self._resolve_property(),
                value=source
            ) if self.predicate not in SKIP_VALUE_RESOLVER else source
            return render_property(source, target, context, self.predicate)

        target = await context.value_resolver.async_resolve(
            labels=context.labels[self._resolve_variable()],
            key=self._resolve_property(),
            value=target
        ) if self.predicate not in SKIP_VALUE_RESOLVER else target
        target = flatten(target)
        return render_list(source, target, context, self.predicate)

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
        return OCListPredicateExpression(elements, "within")

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return f"IN {''.join([str(e) for e in self.elements])}"
