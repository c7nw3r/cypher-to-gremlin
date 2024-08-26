from unittest import TestCase

from cypher_to_gremlin.__spi__.classes import Context
from cypher_to_gremlin.cypher_engine import CypherEngine


class CypherToGremlinTest(TestCase):

    def test_simple_match(self):
        engine = CypherEngine.parse("MATCH (asset:Asset) RETURN asset")
        assert engine.to_gremlin() == 'V().hasLabel("Asset")'

    def test_simple_where(self):
        engine = CypherEngine.parse('MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset')
        assert engine.to_gremlin() == 'V().hasLabel("Asset").has("name", "test")'

    def test_simple_where_with_value_resolver(self):
        context = Context(value_resolver=lambda a, b, c: c + "2")
        engine = CypherEngine.parse('MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset')
        assert engine.to_gremlin(context) == 'V().hasLabel("Asset").has("name", "test2")'

    def test_simple_where_with_value_resolver_list(self):
        context = Context(value_resolver=lambda a, b, c: [c + "1", c + "2"])
        engine = CypherEngine.parse('MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset')
        assert engine.to_gremlin(context) == 'V().hasLabel("Asset").has("name", within("test1", "test2"))'

    def test_simple_edge(self):
        engine = CypherEngine.parse("MATCH (product:Product)-[:createdBy]->(vendor:Vendor) RETURN product, vendor")
        assert engine.to_gremlin() == 'V().hasLabel("Product").out("createdBy").hasLabel("Vendor")'

    def test_edge_with_where(self):
        engine = CypherEngine.parse("""
        MATCH (product:Product)-[:createdBy]->(vendor:Vendor) 
        WHERE product.name = "A" and vendor.name = "B"
        RETURN product, vendor
        """)
        assert engine.to_gremlin() == 'V().hasLabel("Product").has("name", "A").out("createdBy").hasLabel("Vendor").has("name", "B")'
