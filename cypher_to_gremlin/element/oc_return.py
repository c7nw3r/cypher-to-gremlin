from typing import List

from cypher_to_gremlin.__spi__.classes import (
    Context,
    CypherElement,
    CypherElementVisitor,
)
from cypher_to_gremlin.__util__.list_util import opt_find
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.oc_limit import OCLimit
from cypher_to_gremlin.element.oc_order import OCOrder
from cypher_to_gremlin.mixin.aggregate_mixin import AggregateMixin
from cypher_to_gremlin.mixin.property_mixin import PropertyVisitor
from cypher_to_gremlin.mixin.variable_mixin import VariableVisitor


class OCReturn(CypherElement, AggregateMixin):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

        self.order = opt_find(elements, OCOrder)
        self.limit = opt_find(elements, OCLimit)

    @property
    def projections(self):
        visitor = PropertyVisitor()
        self.elements[0].accept(visitor)
        projections = list(dict.fromkeys(f'"{e}"' for e in visitor))
        return projections[0:1]

    def execute(self, context: Context) -> str:
        visitor = VariableVisitor()
        self.accept(visitor)

        if self.order is not None:
            segments = [f"{self.order.execute(context)}"]

            if self.limit:
                segments.append(self.limit.execute(context))

            if len(self.projections) > 0:
                segments.append(f".values({','.join(self.projections)})")
            else:
                segments.append(f".select(\"{self.elements[0].var_name}\")")

            return "".join(segments)

        if len(self.aggregators) > 0:
            # FIXME
            return f".count()"

        # order preserving deduplication
        var_names = list(dict.fromkeys(f'"{e}"' for e in visitor))
        if len(var_names) > 0:
            return f".select({', '.join(var_names)})"

        return ""

    async def async_execute(self, context: Context) -> str:
        visitor = VariableVisitor()
        self.accept(visitor)

        if self.order is not None:
            segments = [f"{self.order.execute(context)}"]

            if self.limit:
                segments.append(self.limit.execute(context))

            if len(self.projections) > 0:
                segments.append(f".values({','.join(self.projections)})")
            else:
                segments.append(f".select(\"{self.elements[0].var_name}\")")

            return "".join(segments)

        if len(self.aggregators) > 0:
            # FIXME
            return f".count()"

        # order preserving deduplication
        var_names = list(dict.fromkeys(f'"{e}"' for e in visitor))
        if len(var_names) > 0:
            return f".select({', '.join(var_names)})"

        return ""

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_ReturnContext, supplier):
        return OCReturn(supplier(ctx))

    def __repr__(self):
        return f"RETURN {[''.join([str(e) for e in self.elements])]}"
