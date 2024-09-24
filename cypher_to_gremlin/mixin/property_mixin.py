from typing import Optional

from cypher_to_gremlin.__spi__.classes import CypherElement, CypherElementVisitor, Visitable
from cypher_to_gremlin.element.oc_property_lookup import OCPropertyLookup


class PropertyVisitor(CypherElementVisitor, list):
    def visit(self, element: CypherElement):
        if isinstance(element, OCPropertyLookup):
            self.append(element.name)


class PropertyMixin(Visitable):

    @property
    def property_name(self) -> Optional[str]:
        visitor = PropertyVisitor()
        self.accept(visitor)
        return visitor[0] if len(visitor) > 0 else None
