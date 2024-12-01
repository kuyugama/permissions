from functools import lru_cache

from .parse import parse_permission


def _get_sub_schema(schema: dict | list, name: str) -> dict | list | None:
    if isinstance(schema, dict) and name in schema:
        return schema[name]

    for element in schema:
        if element == name:
            return {}

        if isinstance(element, dict) and name in element:
            return element[name]


class Permission:
    def __init__(self, schema: dict | list, parts: tuple[str, ...] = ()):
        self.schema = schema
        self.parts = parts or ""
        self.parts_max_index = len(self.parts) - 1

    @lru_cache
    def _exist_in_schema(self, parts: tuple[str, ...]) -> bool:
        schema = self.schema
        for part in parts:
            schema = _get_sub_schema(schema, part)

            if schema is None:
                return False

        return True

    def sub(self, permission: str | tuple[str, ...]) -> "Permission":
        if isinstance(permission, tuple):
            parts = permission
        else:
            parts = (permission,)

        if self.parts:
            parts = self.parts + parts

        if self._exist_in_schema(parts):
            return Permission(self.schema, parts)

    @property
    def name(self):
        return ".".join(self.parts)

    def match(self, permission: str) -> bool:
        """
        Check if this permission matches the given permission.

        :param permission: Permission to match.
        :return: Match result.
        """
        if isinstance(permission, Permission):
            parts = permission.parts
            parts_max_index = permission.parts_max_index
        else:
            parts = parse_permission(permission)["parts"]
            parts_max_index = len(parts) - 1

        if parts == self.parts:
            return True

        for i, part in enumerate(self.parts):
            if i > parts_max_index:
                break

            if parts[i] != part and not (part == "*" or parts[i] == "*"):
                return False

        return True

    def __getattr__(self, name: str):
        if name in ("_", "__"):
            name = "*"

        return self.sub(name.replace("_", "-"))

    def __getitem__(self, name: str):
        return self.sub(name)

    def __repr__(self):
        return "Permission({})".format(self.name)

    def __str__(self):
        return self.name
