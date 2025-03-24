from typing import Optional

from antlr4 import CommonTokenStream, InputStream

from cypher_to_gremlin.__spi__.classes import Context, CypherElement
from cypher_to_gremlin.__spi__.types import CypherSource
from cypher_to_gremlin.antlr.CypherLexer import CypherLexer
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.cypher_visitor import CypherVisitorImpl
from cypher_to_gremlin.listener.error_listener import CypherErrorListener


def decorate(
        gremlin: str,
        dedup: bool = False,
        to_value_map: bool = False,
        limit: int | None = None
) -> str:
    if dedup:
        gremlin += ".dedup()"
    if to_value_map and "count()" not in gremlin:
        gremlin += ".valueMap(true)"
    if limit is not None:
        gremlin += f".limit({limit})"

    return gremlin


class CypherToGremlin:
    def __init__(self, context: Optional[Context] = None):
        if context is None:
            context = Context()
        self.context = context

    @staticmethod
    def stream(source: CypherSource):
        if isinstance(source, InputStream):
            return source
        if isinstance(source, str):
            return InputStream(str(source))
        if isinstance(source, bytes):
            return InputStream(source.decode("utf-8"))
        if isinstance(source, bytearray):
            return InputStream(source.decode("utf-8"))
        raise ValueError(str(source) + " cannot be converted to input stream")

    def _parse_syntax_tree(self, source: CypherSource) -> list[CypherElement]:
        lexer = CypherLexer(CypherToGremlin.stream(source))
        stream = CommonTokenStream(lexer)
        parser = CypherParser(stream)

        error_listener = CypherErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)

        visitor = CypherVisitorImpl()
        cypher_ctx = parser.oC_Cypher()
        tree = visitor.visit(cypher_ctx)

        if len(error_listener.errors) > 0:
            raise ValueError(str(error_listener.errors[0]))

        return tree

    def execute(
            self,
            source: CypherSource,
            dedup: bool = False,
            to_value_map: bool = False,
            limit: int | None = None
    ) -> str:
        gremlin = "g.V()" + "".join([
            e.execute(self.context)
            for e in self._parse_syntax_tree(source)
        ])
        return decorate(gremlin, dedup, to_value_map, limit)

    async def async_execute(
            self,
            source: CypherSource,
            dedup: bool = False,
            to_value_map: bool = False,
            limit: int | None = None
    ) -> str:
        import asyncio
        results = await asyncio.gather(*[
            e.async_execute(self.context)
            for e in self._parse_syntax_tree(source)
        ])
        return decorate("g.V()" + "".join(results), dedup, to_value_map, limit)
