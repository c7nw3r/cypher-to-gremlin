from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.oc_pattern_part import OCPatternPart


class OCPattern(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        # noinspection PyTypeChecker
        self.elements: List[OCPatternPart] = elements

    def execute(self, context: Context) -> str:
        if len(self.elements) <= 1:
            return self.elements[0].execute(context)

        if len(set([e.source_var for e in self.elements])) == 1:
            # MATCH (document:Document)-[:HAS_KEYWORD]->(kw1:Keyword),
            #       (document)         -[:HAS_KEYWORD]->(kw2:Keyword)
            result = [e.execute(context.with_alias(False)) for e in self.elements]

            return "".join([
                result[0][0],
                *[f'.where({"".join(e[1:])[1:]})' for e in result]
            ])

        raise ValueError("pattern parts with different source nodes are not supported")

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    @staticmethod
    def parse(ctx: CypherParser.OC_PatternContext, supplier):
        return OCPattern(supplier(ctx))

    def __repr__(self):
        return ", ".join([str(e) for e in self.elements])
