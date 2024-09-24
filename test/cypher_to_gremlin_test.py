from unittest import TestCase

from cypher_to_gremlin import Context, CypherToGremlin


class CypherToGremlinTest(TestCase):
    def test_simple_match(self):
        gremlin = CypherToGremlin().to_gremlin("MATCH (asset:Asset) RETURN asset")
        assert gremlin == 'V().hasLabel("Asset").as("asset").select("asset")'

    def test_simple_where(self):
        gremlin = CypherToGremlin().to_gremlin(
            'MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset'
        )
        assert (
            gremlin
            == 'V().hasLabel("Asset").has("name", "test").as("asset").select("asset")'
        )

    def test_simple_where_with_value_resolver(self):
        context = Context(value_resolver=lambda a, b, c: c + "2")
        gremlin = CypherToGremlin(context).to_gremlin(
            'MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset'
        )
        assert (
            gremlin
            == 'V().hasLabel("Asset").has("name", "test2").as("asset").select("asset")'
        )

    def test_simple_where_with_value_resolver_list(self):
        context = Context(value_resolver=lambda a, b, c: [c + "1", c + "2"])
        gremlin = CypherToGremlin(context).to_gremlin(
            'MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset'
        )
        assert (
            gremlin
            == 'V().hasLabel("Asset").has("name", within("test1", "test2")).as("asset").select("asset")'
        )

    def test_simple_edge(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (product:Product)-[:createdBy]->(vendor:Vendor)
        RETURN product, vendor
        """)
        assert (
            gremlin
            == 'V().hasLabel("Product").as("product").out("createdBy").hasLabel("Vendor").as("vendor").select("product", "vendor")'
        )

    def test_edge_with_where(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (product:Product)-[:createdBy]->(vendor:Vendor)
        WHERE product.name = "A" and vendor.name = "B"
        RETURN product, vendor
        """)
        assert (
            gremlin
            == 'V().hasLabel("Product").has("name", "A").as("product").out("createdBy").hasLabel("Vendor").has("name", "B").as("vendor").select("product", "vendor")'
        )

    def test_edge_with_multiple_types(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (document:Document)-[r:HAS_TOPIC|HAS_KEYWORD]->(n) WHERE n.text = "Stahl" RETURN document
        """)
        assert (
            gremlin
            == 'V().hasLabel("Document").as("document").out("HAS_TOPIC", "HAS_KEYWORD").has("text", "Stahl").as("n").select("document")'
        )

    def test_in_list_operator(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (document:Document) WHERE document.type IN ["A", "B", "C"] RETURN document
        """)

        assert (
            gremlin
            == 'V().hasLabel("Document").has("type", within("A", "B", "C")).as("document").select("document")'
        )

    def test_greater_equals_expression(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (document:Document) WHERE document.page_num >= 10 RETURN document
        """)

        assert (
            gremlin
            == 'V().hasLabel("Document").has("page_num", ge(10)).as("document").select("document")'
        )

    def test_count(self):
        gremlin = CypherToGremlin().to_gremlin("""
        MATCH (document:Document) RETURN COUNT(*)
        """)

        assert (
            gremlin
            == 'V().hasLabel("Document").as("document").count()'
        )
