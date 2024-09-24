from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCLiteral(CypherElement):

    def __init__(self, repr: str):
        self.repr = repr

    def execute(self, context: Context) -> str:
        return self.repr

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(ctx: CypherParser.OC_LiteralContext, _supplier):
        return OCLiteral(ctx.getText())

    def __repr__(self):
        return self.repr
