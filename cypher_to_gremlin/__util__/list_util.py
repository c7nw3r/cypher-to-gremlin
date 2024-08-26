from typing import Optional, List

from cypher_to_gremlin.__spi__.classes import CypherElement


def opt_find(array: List[CypherElement], cls) -> Optional[CypherElement]:
    for item in array:
        if isinstance(item, cls):
            return item
    return None


def find(array: List[CypherElement], cls) -> CypherElement:
    for item in array:
        if isinstance(item, cls):
            return item
    raise ValueError("cypher element not found")
