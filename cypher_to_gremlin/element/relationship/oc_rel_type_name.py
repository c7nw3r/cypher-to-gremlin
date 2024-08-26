from cypher_to_gremlin.__spi__.classes import CypherElement, Context
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCRelTypeName(CypherElement):

    def __init__(self, name: str):
        self.name = name

    def execute(self, context: Context) -> str:
        return self.name

    @staticmethod
    def parse(ctx: CypherParser.OC_RelTypeNameContext, supplier):
        return OCRelTypeName(ctx.getText())

    def __repr__(self):
        return f'"{self.name}"'
