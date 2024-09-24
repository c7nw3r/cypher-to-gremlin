from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, CypherElementVisitor, Visitable
from cypher_to_gremlin.element.oc_literal import OCLiteral


class LiteralsVisitor(CypherElementVisitor, list):
    def __init__(self, as_repr: bool = True):
        super().__init__()
        self.as_repr = as_repr

    def visit(self, element: CypherElement):
        if isinstance(element, OCLiteral):
            self.append(element.repr if self.as_repr else element.value)


class LiteralMixin(Visitable):

    @property
    def literals(self) -> List[str]:
        visitor = LiteralsVisitor()
        self.accept(visitor)
        return visitor[0] if len(visitor) > 0 else None
