from unittest import TestCase

from cypher_to_gremlin import CypherToGremlin, Context


class CypherToGremlinTest(TestCase):

    def test_simple_match(self):
        gremlin = CypherToGremlin().to_gremlin("MATCH (asset:Asset) RETURN asset")
        assert gremlin == 'V().hasLabel("Asset")'

    def test_simple_where(self):
        gremlin = CypherToGremlin().to_gremlin('MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset')
        assert gremlin == 'V().hasLabel("Asset").has("name", "test")'

    def test_simple_where_with_value_resolver(self):
        context = Context(value_resolver=lambda a, b, c: c + "2")
        gremlin = CypherToGremlin(context).to_gremlin('MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset')
        assert gremlin == 'V().hasLabel("Asset").has("name", "test2")'

    def test_simple_where_with_value_resolver_list(self):
        context = Context(value_resolver=lambda a, b, c: [c + "1", c + "2"])
        gremlin = CypherToGremlin(context).to_gremlin('MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset')
        assert gremlin == 'V().hasLabel("Asset").has("name", within("test1", "test2"))'

    def test_simple_edge(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (product:Product)-[:createdBy]->(vendor:Vendor) 
        RETURN product, vendor
        """)
        assert gremlin == 'V().hasLabel("Product").out("createdBy").hasLabel("Vendor")'

    def test_edge_with_where(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (product:Product)-[:createdBy]->(vendor:Vendor) 
        WHERE product.name = "A" and vendor.name = "B"
        RETURN product, vendor
        """)
        assert gremlin == 'V().hasLabel("Product").has("name", "A").out("createdBy").hasLabel("Vendor").has("name", "B")'

    def test_edge_with_multiple_types(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (document:Document)-[r:HAS_TOPIC|HAS_KEYWORD]->(n) WHERE n.text = "Stahl" RETURN document
        """)
        assert gremlin == 'V().hasLabel("Document").out("HAS_TOPIC", "HAS_KEYWORD").has("text", "Stahl")'
