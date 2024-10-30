from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCFunctionName(CypherElement):

    def __init__(self, name: str):
        self.name = name

    def execute(self, context: Context) -> str:
        return self.name

    @staticmethod
    def parse(ctx: CypherParser.OC_FunctionNameContext, _supplier):
        return OCFunctionName(ctx.getText())

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    def __repr__(self):
        return self.name
