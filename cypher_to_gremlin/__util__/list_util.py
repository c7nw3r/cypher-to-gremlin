from typing import Optional, List, Union

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

def flatten(array: list[Union[any, list]]) -> list:
    if not array:
        return array

    if len(array) > 0 and isinstance(array[0], list):
        return [e for subset in array for e in subset]

    return array