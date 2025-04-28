class EntityFieldVariable:
    entity_type: str
    variables: dict[str, str]

    def __init__(self, entity_type: str, variables: dict[str, str]):
        self.entity_type = entity_type
        self.variables = variables

    def get_fields(self) -> list[str]:
        return list(self.variables.values())

    @staticmethod
    def from_dict(data: dict):
        return EntityFieldVariable(
            data.get("entity_type", ""), data.get("variables", {})
        )
