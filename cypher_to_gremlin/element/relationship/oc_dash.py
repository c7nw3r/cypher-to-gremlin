from cypher_to_gremlin.__spi__.classes import CypherElement, Context
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCDash(CypherElement):

    def execute(self, context: Context) -> str:
        return None

    @staticmethod
    def parse(ctx: CypherParser.OC_DashContext, _supplier):
        return OCDash()

    def __repr__(self):
        return "-"
