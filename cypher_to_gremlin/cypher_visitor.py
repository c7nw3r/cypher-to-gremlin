from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.antlr.CypherVisitor import CypherVisitor
from cypher_to_gremlin.element.expression.oc_and_expression import OCAndExpression
from cypher_to_gremlin.element.expression.oc_comparison_expression import (
    OCComparisonExpression,
)
from cypher_to_gremlin.element.expression.oc_partial_comparison_expression import (
    OCPartialComparisonExpression,
)
from cypher_to_gremlin.element.expression.oc_string_list_null_predicate_expression import (
    OCStringListNullPredicateExpression,
)
from cypher_to_gremlin.element.oc_literal import OCLiteral
from cypher_to_gremlin.element.oc_match import OCMatch
from cypher_to_gremlin.element.oc_node_label import OCNodeLabel
from cypher_to_gremlin.element.oc_node_pattern import OCNodePattern
from cypher_to_gremlin.element.oc_pattern import OCPattern
from cypher_to_gremlin.element.oc_pattern_part import OCPatternPart
from cypher_to_gremlin.element.oc_property_lookup import OCPropertyLookup
from cypher_to_gremlin.element.oc_return import OCReturn
from cypher_to_gremlin.element.oc_single_query import OCSingleQuery
from cypher_to_gremlin.element.oc_variable import OCVariable
from cypher_to_gremlin.element.oc_where import OCWhere
from cypher_to_gremlin.element.relationship.oc_dash import OCDash
from cypher_to_gremlin.element.relationship.oc_left_arrow_head import OCLeftArrowHead
from cypher_to_gremlin.element.relationship.oc_rel_type_name import OCRelTypeName
from cypher_to_gremlin.element.relationship.oc_relationship_detail import (
    OCRelationshipDetail,
)
from cypher_to_gremlin.element.relationship.oc_relationship_pattern import (
    OCRelationshipPattern,
)
from cypher_to_gremlin.element.relationship.oc_right_arrow_head import OCRightArrowHead


class CypherVisitorImpl(CypherVisitor):

    def visitOC_SingleQuery(self, ctx: CypherParser.OC_SingleQueryContext):
        return OCSingleQuery.parse(ctx, super().visitOC_SingleQuery)

    def visitOC_Match(self, ctx: CypherParser.OC_MatchContext):
        return OCMatch.parse(ctx, super().visitOC_Match)

    def visitOC_Pattern(self, ctx: CypherParser.OC_PatternContext):
        return OCPattern.parse(ctx, super().visitOC_Pattern)

    def visitOC_PatternPart(self, ctx: CypherParser.OC_PatternPartContext):
        return OCPatternPart.parse(ctx, super().visitOC_Pattern)

    def visitOC_Variable(self, ctx: CypherParser.OC_VariableContext):
        return OCVariable.parse(ctx, super().visitOC_Variable)

    def visitOC_NodePattern(self, ctx: CypherParser.OC_NodePatternContext):
        return OCNodePattern.parse(ctx, super().visitOC_NodePattern)

    def visitOC_NodeLabel(self, ctx: CypherParser.OC_NodeLabelContext):
        return OCNodeLabel.parse(ctx, super().visitOC_NodeLabel)

    def visitOC_Return(self, ctx: CypherParser.OC_ReturnContext):
        return OCReturn.parse(ctx, super().visitOC_Return)

    def visitOC_Where(self, ctx: CypherParser.OC_WhereContext):
        return OCWhere.parse(ctx, super().visitOC_Where)

    def visitOC_PartialComparisonExpression(
        self, ctx: CypherParser.OC_PartialComparisonExpressionContext
    ):
        return OCPartialComparisonExpression.parse(
            ctx, super().visitOC_PartialComparisonExpression
        )

    def visitOC_Literal(self, ctx: CypherParser.OC_LiteralContext):
        return OCLiteral.parse(ctx, super().visitOC_Literal)

    def visitOC_PropertyLookup(self, ctx: CypherParser.OC_PropertyLookupContext):
        return OCPropertyLookup.parse(ctx, super().visitOC_PropertyLookup)

    def visitOC_StringListNullPredicateExpression(
        self, ctx: CypherParser.OC_StringListNullPredicateExpressionContext
    ):
        return OCStringListNullPredicateExpression.parse(
            ctx, super().visitOC_StringListNullPredicateExpression
        )

    def visitOC_RelationshipPattern(
        self, ctx: CypherParser.OC_RelationshipPatternContext
    ):
        return OCRelationshipPattern.parse(ctx, super().visitOC_RelationshipPattern)

    def visitOC_RelationshipDetail(
        self, ctx: CypherParser.OC_RelationshipDetailContext
    ):
        return OCRelationshipDetail.parse(ctx, super().visitOC_RelationshipDetail)

    def visitOC_RelTypeName(self, ctx: CypherParser.OC_RelTypeNameContext):
        return OCRelTypeName.parse(ctx, super().visitOC_RelTypeName)

    def visitOC_LeftArrowHead(self, ctx: CypherParser.OC_LeftArrowHeadContext):
        return OCLeftArrowHead.parse(ctx, super().visitOC_LeftArrowHead)

    def visitOC_RightArrowHead(self, ctx: CypherParser.OC_RightArrowHeadContext):
        return OCRightArrowHead.parse(ctx, super().visitOC_RightArrowHead)

    def visitOC_Dash(self, ctx: CypherParser.OC_DashContext):
        return OCDash.parse(ctx, super().visitOC_Dash)

    def visitOC_AndExpression(self, ctx: CypherParser.OC_AndExpressionContext):
        return OCAndExpression.parse(ctx, super().visitOC_AndExpression)

    def visitOC_ComparisonExpression(
        self, ctx: CypherParser.OC_ComparisonExpressionContext
    ):
        return OCComparisonExpression.parse(ctx, super().visitOC_ComparisonExpression)

    def aggregateResult(self, aggregate, next_result):
        array = []
        if aggregate is not None:
            array += aggregate
        if next_result is not None:
            if isinstance(next_result, list):
                array.extend(next_result)
            else:
                array += [next_result]
        return array
