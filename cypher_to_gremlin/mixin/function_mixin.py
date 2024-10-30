from dataclasses import dataclass
from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, CypherElementVisitor
from cypher_to_gremlin.element.function.oc_function_invocation import OCFunctionInvocation


@dataclass
class FunctionCall:
    name: str
    args: List[CypherElement]


class FunctionVisitor(CypherElementVisitor, list):
    def visit(self, element: CypherElement):
        if isinstance(element, OCFunctionInvocation):
            self.append(FunctionCall(
                name=str(element.elements[0]),
                args=element.elements[1:]
            ))
