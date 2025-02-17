from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.oc_literal import OCLiteral
from cypher_to_gremlin.element.oc_property_lookup import OCPropertyLookup
from cypher_to_gremlin.mixin.property_mixin import PropertyVisitor
from cypher_to_gremlin.mixin.variable_mixin import VariableMixin


def get_source(element: CypherElement, context: Context):
    if isinstance(element, OCLiteral):
        return element.execute(context).replace("'", '"')

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
            return f'.filter(values("{target.name}").unfold().is(containing({source})))'

        return f'.has("{source}", within({", ".join(target)}))'

    @staticmethod
    def parse(ctx: CypherParser.OC_ListPredicateExpressionContext, supplier):
        elements = supplier(ctx)
        return OCListPredicateExpression(elements)

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return f"IN {''.join([str(e) for e in self.elements])}"
