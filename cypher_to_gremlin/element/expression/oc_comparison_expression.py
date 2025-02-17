from typing import List

from cypher_to_gremlin.__spi__.classes import Context, CypherElement, CypherElementVisitor
from cypher_to_gremlin.__util__.str_util import decorate_literal
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.mixin.literals_mixin import LiteralsVisitor
from cypher_to_gremlin.mixin.operator_mixin import OperatorVisitor
from cypher_to_gremlin.mixin.property_mixin import PropertyVisitor
from cypher_to_gremlin.mixin.variable_mixin import VariableMixin, VariableVisitor


class OCComparisonExpression(CypherElement, VariableMixin):
    def __init__(self, elements: List[CypherElement]):
        self.elements = elements

    def execute(self, context: Context) -> str:
        _variable = self._resolve_variable()
        _property = self._resolve_property()
        _literals = self._resolve_literals()
        _operator = self._resolve_operator()

        value = context.value_resolver(
            context.labels[_variable], _property, _literals
        )

        if isinstance(value, list):
            values = ", ".join([decorate_literal(e) for e in value])
            if context.dialect == "gremlinpython":
                return f'.has("{_property}", within([{values}]))'
            return f'.has("{_property}", within({values}))'

        if _operator is None:
            return f'.has("{_property}", {decorate_literal(value)})'
        if _operator == "=":
            return f'.has("{_property}", {decorate_literal(value)})'
        if _operator == ">=":
            return f'.has("{_property}", ge({decorate_literal(value)}))'
        if _operator == ">":
            return f'.has("{_property}", gt({decorate_literal(value)}))'
        if _operator == "<=":
            return f'.has("{_property}", le({decorate_literal(value)}))'
        if _operator == "<":
            return f'.has("{_property}", lt({decorate_literal(value)}))'
        if _operator == "IS NULL":
            return f'.has("{_property}", "__NULL__")'
        if _operator == "IS NOT NULL":
            return f'.not(has("{_property}", "__NULL__"))'

        raise ValueError("invalid operator " + _operator)

    def _resolve_variable(self):
        visitor = VariableVisitor()
        [e.accept(visitor) for e in self.elements]
        return visitor[0] if len(visitor) > 0 else None

    def _resolve_property(self):
        visitor = PropertyVisitor()
        [e.accept(visitor) for e in self.elements]
        return visitor[0] if len(visitor) > 0 else None

    def _resolve_literals(self):
        visitor = LiteralsVisitor(as_repr=False)
        [e.accept(visitor) for e in self.elements]
        return visitor[0] if len(visitor) == 1 else visitor if len(visitor) > 0 else None

    def _resolve_operator(self):
        visitor = OperatorVisitor()
        [e.accept(visitor) for e in self.elements]
        return visitor[0] if len(visitor) > 0 else None

    @staticmethod
    def parse(ctx: CypherParser.OC_ComparisonExpressionContext, supplier):
        elements = supplier(ctx)
        return OCComparisonExpression(elements) if len(elements) > 1 else elements

    def accept(self, visitor: CypherElementVisitor):
        visitor.visit(self)
        [e.accept(visitor) for e in self.elements]

    def __repr__(self):
        return " ".join([str(e) for e in self.elements])
