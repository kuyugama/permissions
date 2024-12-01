import time

from permissions import Permission
from permissions.parse import parse_schema

raw_schema = """*
content.raw.decode
content.encode
content.*
user.own.update-info
user.update-info
user.*
"""

schema = parse_schema(raw_schema)


permissions = Permission(schema)  # type: ignore

required_permission = permissions.user.own.update_info
available_permission = permissions.user.__

assert required_permission.match(available_permission)
assert required_permission.parts == ("user", "own", "update-info")
assert available_permission.parts == ("user", "*")

assert permissions.sub(("user", "own", "update-info")) is not None
assert permissions.sub(("user", "not-exists")) is None


match = (
    (permissions.user.own.update_info, permissions.user.__),
    (permissions.content.raw.decode, permissions.content.__),
    (permissions.content.__, permissions.content.raw.decode),
    (permissions.user.__, permissions.user.own.update_info),
    (permissions.__, permissions.user.own.update_info),
    (permissions.user.own.update_info, permissions.__),
    (permissions.user.own.update_info, permissions.user.own.update_info),
    (permissions.content.raw, permissions.content.raw),
    (permissions.user.own, permissions.user.own),
    (permissions.content, permissions.content),
    (permissions.user.__, permissions.content.__),
    (permissions.user, permissions.content.__),
    (permissions.user, permissions.content),
    (permissions.user, permissions.user),
)

f = 30
s = 30
m = 11
print(
    "FIRST".center(f) + "| " + "SECOND".center(s) + "| " + "MATCHES".center(m),
    *(
        str(first).ljust(f) + "| " + str(second).ljust(s) + '| ' + str(first.match(second)).center(m)
        for first, second in match
    ),
    sep=" |\n",
    end=" |\n" + "-" * (f + s + m  + 6) + "\n"
)


if __name__ == "__main__":
    from permissions.generate import generate_pyi_file

    generate_pyi_file(schema, __file__ + "i")
