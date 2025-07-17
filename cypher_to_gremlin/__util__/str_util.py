def decorate_literal(literal: any):
    if isinstance(literal, str):
        if literal[0] == '"' and literal[-1] == '"':
            return literal
        if literal[0] == "'" and literal[-1] == "'":
            return literal.replace("'", '"')
        return f'"{literal}"'
    return literal
