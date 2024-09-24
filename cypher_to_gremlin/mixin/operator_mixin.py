from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, CypherElementVisitor, Visitable
from cypher_to_gremlin.element.expression.oc_partial_comparison_expression import OCPartialComparisonExpression


class OperatorVisitor(CypherElementVisitor, list):
    def visit(self, element: CypherElement):
        if isinstance(element, OCPartialComparisonExpression):
            self.append(element.operator)


class OperatorMixin(Visitable):

    @property
    def literals(self) -> List[str]:
        visitor = OperatorVisitor()
        self.accept(visitor)
        return visitor[0] if len(visitor) > 0 else None
