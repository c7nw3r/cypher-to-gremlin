from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, AsyncCharSequence, \
    CharSequence
from cypher_to_gremlin.antlr.CypherParser import CypherParser


class OCNullPredicateExpression(CypherElement):

    def __init__(self, negated: bool):
        self.negated = negated

    def execute(self, context: Context) -> CharSequence:
        return "IS NOT NULL" if self.negated else "IS NULL"

    async def async_execute(self, context: Context) -> AsyncCharSequence:
        return "IS NOT NULL" if self.negated else "IS NULL"

    @staticmethod
    def parse(ctx: CypherParser.OC_NullPredicateExpressionContext, _supplier):
        return OCNullPredicateExpression("not" in ctx.getText().lower())

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    def __repr__(self):
        return "IS NOT NULL" if self.negated else "IS NULL"
