from typing import List

from cypher_to_gremlin.__spi__.classes import Context, CypherElement
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCReturn(CypherElement):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        segments = [f'"{elem.var_name}"' for elem in self.elements if elem.var_name]

        if segments:
            return f".select({", ".join(segments)})"

        return ""

    @staticmethod
    def parse(ctx: CypherParser.OC_ReturnContext, supplier):
        return OCReturn(supplier(ctx))

    def __repr__(self):
        return f"RETURN {[''.join([str(e) for e in self.elements])]}"
