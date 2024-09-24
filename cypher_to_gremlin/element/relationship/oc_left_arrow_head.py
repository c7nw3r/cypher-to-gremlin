from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCLeftArrowHead(CypherElement):

    def execute(self, context: Context) -> str:
        return None

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(ctx: CypherParser.OC_LeftArrowHeadContext, _supplier):
        return OCLeftArrowHead()

    def __repr__(self):
        return "<-"
