from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.relationship.oc_left_arrow_head import OCLeftArrowHead
from cypher_to_gremlin.element.relationship.oc_relationship_detail import (
    OCRelationshipDetail,
)
from cypher_to_gremlin.element.relationship.oc_right_arrow_head import OCRightArrowHead


class OCRelationshipPattern(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.rel_details = [e for e in elements if isinstance(e, OCRelationshipDetail)][
            0
        ]
        self.is_outgoing = any([isinstance(e, OCRightArrowHead) for e in elements])
        self.is_incoming = any([isinstance(e, OCLeftArrowHead) for e in elements])

    def execute(self, context: Context) -> str:
        if self.is_outgoing and self.is_incoming:
            return f".both({', '.join([str(e) for e in self.rel_details.type_names])})"
        if self.is_outgoing:
            return f".out({', '.join([str(e) for e in self.rel_details.type_names])})"
        if self.is_incoming:
            return f".in({', '.join([e.name for e in self.rel_details.type_names])})"
        raise ValueError("not implemented")

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        self.rel_details.accept(visitor)

    @staticmethod
    def parse(ctx: CypherParser.OC_RelationshipPatternContext, supplier):
        return OCRelationshipPattern(supplier(ctx))

    def __repr__(self):
        if self.is_incoming and self.is_outgoing:
            return f"-{self.rel_details}-"
        if self.is_incoming:
            return f"<-{self.rel_details}-"
        return f"-{self.rel_details}->"


        return f"{''.join([str(e) for e in self.rel_details])}"
