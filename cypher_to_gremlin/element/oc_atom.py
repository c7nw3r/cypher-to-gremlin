from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, CharSequence, \
    AsyncCharSequence
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCAtom(CypherElement):

    def __init__(self, repr: str):
        self.repr = repr

    def execute(self, context: Context) -> CharSequence:
        return self.repr

    async def async_execute(self, context: Context) -> AsyncCharSequence:
        return self.repr

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(ctx: CypherParser.OC_AtomContext, supplier):
        elements = supplier(ctx)
        if "count" in ctx.getText().lower():
            return OCAtom(ctx.getText())
        return elements

    def __repr__(self):
        return self.repr
