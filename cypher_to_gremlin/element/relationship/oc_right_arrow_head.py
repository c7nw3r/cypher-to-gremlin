from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCRightArrowHead(CypherElement):

    def execute(self, context: Context) -> str:
        return None

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(_ctx: CypherParser.OC_RightArrowHeadContext, _supplier):
        return OCRightArrowHead()

    def __repr__(self):
        return "->"
