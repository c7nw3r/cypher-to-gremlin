from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, StringLike, CharSequence
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.mixin.variable_mixin import VariableVisitor


class OCPatternPart(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    @property
    def source_var(self):
        visitor = VariableVisitor()
        self.elements[0].accept(visitor)
        return visitor[0]

    @property
    def target_var(self):
        visitor = VariableVisitor()
        self.elements[-1].accept(visitor)
        return visitor[0]

    def execute(self, context: Context) -> CharSequence:
        return StringLike([e.execute(context) for e in self.elements])

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_PatternPartContext, supplier):
        return OCPatternPart(supplier(ctx))

    def __repr__(self):
        return "".join([str(e) for e in self.elements])
