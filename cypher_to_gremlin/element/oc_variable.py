from cypher_to_gremlin.__spi__.classes import Context, CypherElement, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCVariable(CypherElement):
    def __init__(self, name: str):
        self.name = name

    def execute(self, context: Context) -> str:
        return self.name

    @property
    def var_name(self) -> str:
        return self.name

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(ctx: CypherParser.OC_VariableContext, _supplier):
        return OCVariable(ctx.getText())

    def __repr__(self):
        return self.name
