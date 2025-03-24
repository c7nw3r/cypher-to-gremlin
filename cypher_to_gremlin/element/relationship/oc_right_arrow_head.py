from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, CharSequence, \
    AsyncCharSequence
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCRightArrowHead(CypherElement):

    def execute(self, context: Context) -> CharSequence:
        return ""

    async def async_execute(self, context: Context) -> AsyncCharSequence:
        return ""

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(_ctx: CypherParser.OC_RightArrowHeadContext, _supplier):
        return OCRightArrowHead()

    def __repr__(self):
        return "->"
