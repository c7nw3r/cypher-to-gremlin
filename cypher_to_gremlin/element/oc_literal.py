from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCLiteral(CypherElement):

    def __init__(self, repr: str):
        self.repr = repr

        if '"' in repr:  # str
            self.value = repr[1:-1]
        elif '.' in repr:  # float
            self.value = float(repr)
        elif repr in ["true", "false"]:  # bool
            self.value = repr == "true"
        else:  # int
            self.value = int(repr)

    def execute(self, context: Context) -> str:
        return self.repr

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(ctx: CypherParser.OC_LiteralContext, _supplier):
        text = ctx.getText()
        if text.startswith("["):
            text = text[1:-1]
            return [OCLiteral(e.strip()) for e in text.split(",")]

        return OCLiteral(ctx.getText())

    def __repr__(self):
        return self.repr
