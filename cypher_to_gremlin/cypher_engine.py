from abc import ABC
from typing import List, Optional

from antlr4 import InputStream, CommonTokenStream

from cypher_to_gremlin.__spi__.classes import CypherElement, Context
from cypher_to_gremlin.__spi__.types import CypherSource
from cypher_to_gremlin.antlr.CypherLexer import CypherLexer
from cypher_to_gremlin.antlr.CypherParser import CypherParser
from cypher_to_gremlin.cypher_visitor import CypherVisitorImpl
from cypher_to_gremlin.listener.error_listener import CypherErrorListener


class CypherToGremlin(ABC):

    def __init__(self, tree: List[CypherElement]):
        self.tree = tree
        self.custom_fun = {}

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

    @staticmethod
    def parse(source: CypherSource) -> 'CypherToGremlin':
        lexer = CypherLexer(CypherToGremlin.stream(source))
        stream = CommonTokenStream(lexer)
        parser = CypherParser(stream)

        error_listener = CypherErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        lexer.removeErrorListeners()
        lexer.addErrorListener(error_listener)

        visitor = CypherVisitorImpl()
        tree = visitor.visit(parser.oC_Cypher())

        if len(error_listener.errors) > 0:
            raise ValueError(str(error_listener.errors[0]))

        return CypherToGremlin(tree)

    def to_gremlin(self, context: Optional[Context] = None) -> str:
        return "V()" + "".join([e.execute(context or Context()) for e in self.tree])

    @staticmethod
    def convert(source: CypherSource, context: Optional[Context] = None) -> str:
        return CypherToGremlin.parse(source).to_gremlin(context)
