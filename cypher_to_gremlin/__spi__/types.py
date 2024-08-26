from typing import Union, Literal

from antlr4 import InputStream

CypherSource = Union[InputStream, str, bytes, bytearray]
Operator = Literal["=", "<>", "<", ">", "<=", ">="]
Value = Union[str]
