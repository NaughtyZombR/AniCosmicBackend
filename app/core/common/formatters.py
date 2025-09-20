def to_snake_case(text: str) -> str:
    return "".join(f"_{i.lower()}" if i.isupper() else i for i in text).lstrip(
        "_"
    )
