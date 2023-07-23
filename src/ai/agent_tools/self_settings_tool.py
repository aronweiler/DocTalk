import json
from ai.agent_tools.utilities.abstract_tool import AbstractTool


class SelfSettingsTool(AbstractTool):
    def configure(
        self, registered_settings, memory=None, override_llm=None, json_args=None
    ) -> None:
        """settings should be a dictionary of settings, where the key is the name of the setting, and the value is the setting itself"""
        if registered_settings is None:
            raise Exception("SelfSettingsTool requires settings to be passed in")

        self.registered_settings = registered_settings

    def run(self, query: str) -> str:
        print("SelfSettingsTool got query: " + query)
        # Parse the query
        things_to_set = query.split(",")

        status = []
        # Loop through the query dict and set the settings
        for assignments in things_to_set:
            setting = assignments.split("=")[0].strip()
            value = assignments.split("=")[1].strip()
            self.registered_settings.set_setting(setting, value)
            status.append(f"Set {setting} to {value}")

        return "\n".join(status)

    def get_settings(self):
        return None
