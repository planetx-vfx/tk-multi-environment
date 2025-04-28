from tank import Template


class TemplateVariable:
    name: str
    template: Template

    def __init__(self, name: str, template: Template):
        self.name = name
        self.template = template
