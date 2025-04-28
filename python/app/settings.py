from __future__ import annotations

from .entity_field_variable import EntityFieldVariable
from .template_variable import TemplateVariable


class Settings:
    """
    App configuration
    """

    field_variables: list[EntityFieldVariable]
    template_variables: list[TemplateVariable]

    extra_fields: dict[str, list[str]] = {}

    def __init__(self, app):
        self._app = app

        field_variables = self._app.get_setting("field_variables")
        self.field_variables = []
        for fv in field_variables:
            self.field_variables.append(EntityFieldVariable.from_dict(fv))

        template_variables = self._app.get_setting("template_variables")
        self.template_variables = []
        for tv in template_variables:
            template = self._app.engine.sgtk.templates.get(tv.get("template"))
            self.template_variables.append(
                TemplateVariable(tv.get("name", ""), template)
            )

        self._compile_extra_fields()

    def _compile_extra_fields(self):
        """
        Get a dict of all extra fields to request from ShotGrid for specific entities.
        """
        extra_fields: dict[str, list[str]] = {}

        for override in self.field_variables:
            fields = override.get_fields()

            if override.entity_type in extra_fields:
                extra_fields[override.entity_type].extend(fields)
            else:
                extra_fields[override.entity_type] = fields

        # Remove None values
        for entity, fields in extra_fields.items():
            extra_fields[entity] = [field for field in fields if field is not None]

        self.extra_fields = extra_fields

    def validate_fields(self):
        """
        Check if the required fields exist on the entities.
        """
        missing_fields: dict[str, list[str]] = {}

        for entity_type, fields in self.extra_fields.items():
            schema = self._app.shotgun.schema_field_read(entity_type)

            for field in fields:
                if field not in schema:
                    if entity_type in missing_fields:
                        missing_fields[entity_type].append(field)
                    else:
                        missing_fields[entity_type] = [field]

        if not missing_fields:
            return

        msg = "Some fields that are configured, don't exist on the requested entities:"

        for entity_type, fields in missing_fields.items():
            msg += f"\n    {entity_type}: {', '.join(fields)}"

        raise ValueError(msg)

    def get_extra_fields(self, entity_type: str) -> list[str]:
        return self.extra_fields.get(entity_type, [])

    def get_field_variables(self, entity_type: str):
        variables = {}
        for fv in self.field_variables:
            if fv.entity_type != entity_type:
                continue

            variables.update(fv.variables)

        return variables
