from typing import List

from cypher_to_gremlin.__spi__.classes import CypherElement, Context, CypherElementVisitor, CharSequence, \
    AsyncCharSequence
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.element.relationship.oc_rel_type_name import OCRelTypeName


class OCRelationshipDetail(CypherElement):

    def __init__(self, elements: List[CypherElement]):
        self.type_names = [e for e in elements if isinstance(e, OCRelTypeName)]

    def execute(self, context: Context) -> CharSequence:
        return self.repr

    async def async_execute(self, context: Context) -> AsyncCharSequence:
        return self.repr

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)

    @staticmethod
    def parse(ctx: CypherParser.OC_RelationshipDetailContext, supplier):
        return OCRelationshipDetail(supplier(ctx))

    def __repr__(self):
        return f"[:{', '.join([e.name for e in self.type_names])}]"
