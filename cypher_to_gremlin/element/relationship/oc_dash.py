from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, AsyncCharSequence, \
    CharSequence
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCDash(CypherElement):

    def execute(self, context: Context) -> CharSequence:
        return ""

    async def async_execute(self, context: Context) -> AsyncCharSequence:
        return ""

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(_ctx: CypherParser.OC_DashContext, _supplier):
        return OCDash()

    def __repr__(self):
        return "-"
