from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, CharSequence, \
    AsyncCharSequence
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCRelTypeName(CypherElement):

    def __init__(self, name: str):
        self.name = name

    def execute(self, context: Context) -> CharSequence:
        return self.name

    async def async_execute(self, context: Context) -> AsyncCharSequence:
        return self.name

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(ctx: CypherParser.OC_RelTypeNameContext, _supplier):
        return OCRelTypeName(ctx.getText())

    def __repr__(self):
        return f'"{self.name}"'
