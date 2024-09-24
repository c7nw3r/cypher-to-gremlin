from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, CypherElementVisitor, Visitable
from cypher_to_gremlin.element.oc_atom import OCAtom


class AggregateVisitor(CypherElementVisitor, list):
    def visit(self, element: CypherElement):
        if isinstance(element, OCAtom) and "count" in element.repr.lower():
            self.append(element.repr)


class AggregateMixin(Visitable):

    @property
    def aggregators(self) -> List[str]:
        visitor = AggregateVisitor()
        self.accept(visitor)
        return visitor
