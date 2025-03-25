from cypher_to_gremlin.__spi__.classes import CypherElementVisitor, Context, CypherElement
from cypher_to_gremlin.element.oc_node_label import OCNodeLabel
from cypher_to_gremlin.element.oc_node_pattern import OCNodePattern


class LabelsVisitor(CypherElementVisitor, dict[str, list[str]]):
    def __init__(self, context: Context):
        super().__init__()
        self.context = context

    def visit(self, element: CypherElement):
        if isinstance(element, OCNodePattern):
            var_name = element.elements[0].execute(self.context)
            labels = [
                e.execute(self.context) for e in element.elements if isinstance(e, OCNodeLabel)
            ]

            self[var_name] = [e[1:-1] for e in labels]
