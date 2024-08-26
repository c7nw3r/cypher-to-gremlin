from cypher_to_gremlin.__spi__.classes import CypherElement, Context
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCRightArrowHead(CypherElement):

    def execute(self, context: Context) -> str:
        return None

    @staticmethod
    def parse(ctx: CypherParser.OC_RightArrowHeadContext, _supplier):
        return OCRightArrowHead()

    def __repr__(self):
        return "->"
