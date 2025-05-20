from unittest import TestCase

from cypher_to_gremlin import Context, CypherToGremlin
from cypher_to_gremlin.__spi__.protocols import NoOpValueResolver
from cypher_to_gremlin.value_resolver.delegate_value_resolver import DelegateValueResolver


class CypherToGremlinTest(TestCase):
    def test_simple_match(self):
        gremlin = CypherToGremlin().execute("MATCH (asset:Asset) RETURN asset")
        assert gremlin == 'g.V().hasLabel("Asset").as("asset").select("asset")'

    def test_simple_where(self):
        gremlin = CypherToGremlin().execute(
            'MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset'
        )
        print(gremlin)
        assert (
                gremlin
                == 'g.V().hasLabel("Asset").has("name", "test").as("asset").select("asset")'
        )

    def test_simple_where_with_value_resolver(self):
        context = Context(value_resolver=DelegateValueResolver(lambda a, b, c: c + "2"))
        gremlin = CypherToGremlin(context).execute(
            'MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset'
        )
        assert (
                gremlin
                == 'g.V().hasLabel("Asset").has("name", "test2").as("asset").select("asset")'
        )

    def test_simple_where_with_batch_value_resolver(self):
        context = Context(value_resolver=DelegateValueResolver(lambda a, b, c: c + "2"))
        gremlin = CypherToGremlin(context).execute(
            'MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset',
            batch=True
        )
        assert (
                gremlin
                == 'g.V().hasLabel("Asset").has("name", "test2").as("asset").select("asset")'
        )

    def test_simple_where_with_value_resolver_list(self):
        context = Context(value_resolver=DelegateValueResolver(lambda a, b, c: [c + "1", c + "2"]))
        gremlin = CypherToGremlin(context).execute(
            'MATCH (asset:Asset) WHERE asset.name = "test" RETURN asset'
        )
        assert (
                gremlin
                == 'g.V().hasLabel("Asset").has("name", within("test1", "test2")).as("asset").select("asset")'
        )

    def test_simple_edge(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (product:Product)-[:createdBy]->(vendor:Vendor)
        RETURN product, vendor
        """)
        assert (
                gremlin
                == 'g.V().hasLabel("Product").as("product").out("createdBy").hasLabel("Vendor").as("vendor").select("product", "vendor")'
        )

    def test_edge_with_where(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (product:Product)-[:createdBy]->(vendor:Vendor)
        WHERE product.name = "A" and vendor.name = "B"
        RETURN product, vendor
        """)
        assert (
                gremlin
                == 'g.V().hasLabel("Product").has("name", "A").as("product").out("createdBy").hasLabel("Vendor").has("name", "B").as("vendor").select("product", "vendor")'
        )

    def test_edge_with_multiple_types(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (document:Document)-[r:HAS_TOPIC|HAS_KEYWORD]->(n) WHERE n.text = "Stahl" RETURN document
        """)
        assert (
                gremlin
                == 'g.V().hasLabel("Document").as("document").out("HAS_TOPIC", "HAS_KEYWORD").has("text", "Stahl").as("n").select("document")'
        )

    def test_in_list_operator(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (document:Document) WHERE document.type IN ["A", "B", "C"] RETURN document
        """)
        assert (
                gremlin
                == 'g.V().hasLabel("Document").has("type", within("A", "B", "C")).as("document").select("document")'
        )

    def test_greater_equals_expression(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (document:Document) WHERE document.page_num >= 10 RETURN document
        """)

        assert (
                gremlin
                == 'g.V().hasLabel("Document").has("page_num", ge(10)).as("document").select("document")'
        )

    def test_count(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (document:Document) RETURN COUNT(*)
        """)

        assert gremlin == 'g.V().hasLabel("Document").as("document").count()'

    def test_several_matches(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (document:Document)-[:HAS_KEYWORD]->(kw1:Keyword WHERE kw1.name = "A"),
              (document)         -[:HAS_KEYWORD]->(kw2:Keyword WHERE kw2.name = "B")
        RETURN document
        """)

        self.assertEqual(
            gremlin
            , """
g.V().hasLabel("Document").where(out("HAS_KEYWORD").hasLabel("Keyword").has("name", "A")).where(out("HAS_KEYWORD").hasLabel("Keyword").has("name", "B")).as("document").select("document")
            """.strip()
        )

    def test_several_matches_with_batch(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (document:Document)-[:HAS_KEYWORD]->(kw1:Keyword WHERE kw1.name = "A"),
              (document)         -[:HAS_KEYWORD]->(kw2:Keyword WHERE kw2.name = "B")
        RETURN document
        """, batch=True)

        self.assertEqual(
            gremlin
            , """
g.V().hasLabel("Document").where(out("HAS_KEYWORD").hasLabel("Keyword").has("name", "A")).where(out("HAS_KEYWORD").hasLabel("Keyword").has("name", "B")).as("document").select("document")
            """.strip()
        )

    def test_count_with_alias(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (d:document) RETURN COUNT(d) AS documentCount
        """)

        assert (
                gremlin
                == """
g.V().hasLabel("document").as("d").count()
            """.strip()
        )

    def test_datetime_comparison(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (d:document)
        WHERE datetime(d.valid_until) <= datetime() 
        RETURN COUNT(d) AS documentCount
        """)

        self.assertEqual(gremlin, 'g.V().hasLabel("document").has("valid_until", le(datetime())).as("d").count()')

    def test_is_null(self):
        gremlin = CypherToGremlin().execute("""
        MATCH (d:document)
        WHERE d.valid_until is null 
        RETURN COUNT(d) AS documentCount
        """)

        self.assertEqual(gremlin, 'g.V().hasLabel("document").has("valid_until", "__NULL__").as("d").count()')

    def test_is_not_null(self):
        gremlin = CypherToGremlin().execute("""
            MATCH (d:document)
            WHERE d.valid_until is not null 
            RETURN COUNT(d) AS documentCount
            """)

        self.assertEqual(gremlin, 'g.V().hasLabel("document").not(has("valid_until", "__NULL__")).as("d").count()')

    def test_or_expression(self):
        gremlin = CypherToGremlin().execute("""
            MATCH (d:document) 
            WHERE (d.document_owner = 'Thomas Hirschegger' OR 'Thomas Hirschegger' IN d.document_assigned_to) 
            RETURN d
            """)

        self.assertEqual(
            'g.V().hasLabel("document").or(has("document_owner", "Thomas Hirschegger"), has("document_assigned_to", "Thomas Hirschegger")).as("d").select("d")',
            gremlin)

    def test_and_or_expression(self):
        gremlin = CypherToGremlin().execute("""
            MATCH (d:document) 
            WHERE d.document_status = 'Nicht begonnen' 
            AND  (d.document_owner = 'Thomas Hirschegger' OR 'Thomas Hirschegger' IN d.document_assigned_to) 
            RETURN d
            """)

        self.assertEqual(
            'g.V().hasLabel("document").has("document_status", "Nicht begonnen").or(has("document_owner", "Thomas Hirschegger"), has("document_assigned_to", "Thomas Hirschegger")).as("d").select("d")',
            gremlin)

    def test_gremlinpython_and_or_expression(self):
        context = Context(
            dialect="gremlinpython",
            value_resolver=NoOpValueResolver()
        )
        gremlin = CypherToGremlin(context).execute("""
            MATCH (d:document) WHERE \'Max Mustermann\' = d.document_owner OR \'Max Mustermann\' IN d.document_assigned_to RETURN d
            """)

        self.assertEqual(
            'g.V().hasLabel("document").or(has("document_owner", "Max Mustermann"), has("document_assigned_to", "Max Mustermann")).as("d").select("d")',
            gremlin)

    def test_order_by_date(self):
        context = Context(
            dialect="cosmosdb",
            value_resolver=NoOpValueResolver()
        )
        gremlin = CypherToGremlin(context).execute("""
            MATCH (d:document) RETURN d.creation_time ORDER BY d.creation_time DESC LIMIT 1
            """)

        self.assertEqual(
            'g.V().hasLabel("document").as("d").order().by("creation_time", decr).limit(1).values("creation_time")',
            gremlin
        )