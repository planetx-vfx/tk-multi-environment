# MIT License
#
# Copyright (c) 2023 Netherlands Film Academy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import json
import os

import sgtk

from .settings import Settings


class Handler:
    def __init__(self, app):
        self.app = app
        self.current_engine = self.app.engine
        self.logger = self.app.logger
        self.sg = self.current_engine.shotgun
        self.current_context = self.current_engine.context
        self.entity = self.current_context.entity

        self.settings = Settings(app)

        self.settings.validate_fields()

        self.env = {}

        if self.entity is not None:
            # Get data from ShotGrid
            entity_type = self.entity["type"]

            filters = [["id", "is", self.entity["id"]]]

            columns = self.settings.get_extra_fields(entity_type)

            if entity_type == "Shot":
                columns.extend(["sg_cut_in", "sg_cut_out"])

            self.entity_data = self.sg.find_one(entity_type, filters, columns)

        # Set environments
        self.__set_environments()

        # Run engine specific functions
        self.app.execute_hook_method(
            key="helper_hook",
            method_name="setup_environment",
            env=self.env,
        )

    # private methods
    def __set_environments(self):
        """Set ShotGrid environment variables"""
        env = {}

        template_variables = self.app.get_setting("template_variables")
        self.logger.debug(template_variables)

        project_name = self.current_context.project.get("name")

        project_data = self.sg.find_one(
            "Project",
            [["name", "is", project_name]],
            self.settings.get_extra_fields("Project"),
        )

        env["SG_PROJECT_NAME"] = project_name
        env["SG_PROJECT_ROOT"] = self.__fix_path(
            self.current_context._get_project_roots()[0]
        )
        env["SG_USER_NAME"] = self.current_context.user.get("name")
        env["SG_USER_ID"] = self.current_context.user.get("id")

        for key, value in self.settings.get_field_variables("Project").items():
            env[key] = project_data.get(value)

        fields: dict = self.current_context.to_dict()

        if self.entity:
            entity_name = self.entity["name"]
            entity_type = self.entity["type"]
            entity_id = self.entity["id"]

            for key, value in self.settings.get_field_variables(entity_type).items():
                env[key] = self.entity_data.get(value)

            env["SG_CONTEXT_TYPE"] = entity_type
            env["SG_CONTEXT_ID"] = entity_id

            template = self.app.get_template("context_root_template")
            fields.update(self.current_context.as_template_fields(template))
            root = self.__fix_path(template.apply_fields(fields))

            work_template = self.app.get_template("work_file_template")
            if work_template:
                file = self.app.execute_hook_method(
                    key="helper_hook",
                    method_name="get_file_path",
                )
                try:
                    fields.update(work_template.get_fields(file))
                    env["SG_NAME"] = fields.get("name")
                    env["SG_VERSION"] = fields.get("version")
                    env["SG_VERSION_S"] = f"v{fields.get('version'):03}"
                except Exception as error:
                    self.logger.error(
                        'Could not resolve fields from current work file "%s": %s',
                        file,
                        error,
                    )

            env["SG_STEP"] = fields.get("Step")
            env["SG_TASK"] = fields.get("Task")
            env[f"SG_{entity_type.upper()}"] = entity_name
            env[f"SG_{entity_type.upper()}_ROOT"] = root

            if entity_type == "Shot":
                env["SG_SEQUENCE"] = fields.get("Sequence")

                env["SG_FSTART"] = self.entity_data.get("sg_cut_in")
                env["SG_FEND"] = self.entity_data.get("sg_cut_out")

            self.logger.debug("Current context for templates: %s", fields)

            for tv in self.settings.template_variables:
                try:
                    path = tv.template.apply_fields(fields)
                    env[tv.name] = self.__fix_path(path)
                except Exception as error:
                    self.logger.error(
                        'An error occurred while applying fields to the template "%s": %s',
                        tv.name,
                        error,
                    )

        self.logger.debug(
            f"Setting Houdini ShotGrid environment variables:\n{json.dumps(env, indent=4)}"
        )

        self.env = env
        for key, value in env.items():
            if value is None:
                self.logger.error(
                    'Env var "%s" resulted in a null value, skipping.', key
                )
                continue

            sgtk.util.append_path_to_env_var(key, str(value))

    def __fix_path(self, path: str) -> str:
        """Fix Windows paths"""
        return path.replace(os.sep, "/")
