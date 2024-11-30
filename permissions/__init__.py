class Permission:
    def __init__(self, schema: dict | list, name: str = None):
        self.schema = schema
        self.name = "" or name

    def sub(self, permission: str):
        name = permission
        if self.name:
            name = self.name + "." + permission

        if isinstance(self.schema, dict) and permission in self.schema:
            return Permission(self.schema[permission], name)

        for element in self.schema:
            if element == permission:
                return Permission({}, name)

            if isinstance(element, dict) and permission in element:
                return Permission(element[permission], name)

    def __getattr__(self, name: str):
        if name == "_":
            name = "*"

        return self.sub(name.replace("_", "-"))

    def __getitem__(self, name: str):
        return self.sub(name)

    def __repr__(self):
        return self.name
