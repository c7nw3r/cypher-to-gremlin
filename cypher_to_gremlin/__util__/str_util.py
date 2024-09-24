def decorate_literal(literal: any):
    if isinstance(literal, str):
        return f'"{literal}"'
    return literal
