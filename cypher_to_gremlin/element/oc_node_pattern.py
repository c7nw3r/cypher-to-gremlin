from typing import List

from cypher_to_gremlin.__spi__.classes import Context, CypherElement, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.oc_node_label import OCNodeLabel
from cypher_to_gremlin.element.oc_where import OCWhere
from cypher_to_gremlin.mixin.variable_mixin import VariableMixin


class OCNodePattern(CypherElement, VariableMixin):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        var_name = self.elements[0].execute(context)
        labels = [
            e.execute(context) for e in self.elements if isinstance(e, OCNodeLabel)
        ]

        context.labels[var_name] = [e[1:-1] for e in labels]

        wheres = [
            e for e in self.elements if isinstance(e, OCWhere)
        ]

        filters = [e for e in context.wheres if e.is_sufficient(context)]

        segments = [f".hasLabel({', '.join(labels)})"] if len(labels) > 0 else []

        for _filter in filters:
            segments.append(_filter.execute(context))
            context.wheres.remove(_filter)

        if wheres:
            segments.append(wheres[0].execute(context))

        if segments and context.alias:
            segments.append(f'.as("{var_name}")')

        if len(labels) == 0 and len(filters) == 0:
            segments.append(f'.select("{var_name}")')

        return "".join(segments)

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_NodePatternContext, supplier):
        return OCNodePattern(supplier(ctx))

    def __repr__(self):
        return f"({''.join([str(e) for e in self.elements])})"
