from permissions import Permission
from permissions.parse import parse_schema

raw_schema = """*
content.raw.decode
content.encode
"""

schema = parse_schema(raw_schema)


permissions = Permission(schema, "")  # type: ignore

print(permissions.content)

if __name__ == "__main__":
    from permissions.generate import generate_pyi_file

    generate_pyi_file(schema, __file__ + "i")
