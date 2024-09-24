from typing import Optional

from cypher_to_gremlin.__spi__.classes import CypherElement, CypherElementVisitor, Visitable, Context
from cypher_to_gremlin.element.oc_variable import OCVariable


class VariableVisitor(CypherElementVisitor, list):
    def visit(self, element: CypherElement):
        if isinstance(element, OCVariable):
            self.append(element.var_name)


class VariableMixin(Visitable):

    @property
    def var_name(self) -> Optional[str]:
        visitor = VariableVisitor()
        self.accept(visitor)
        return visitor[0] if len(visitor) > 0 else None

    def is_sufficient(self, context: Context):
        return self.var_name in context.labels
