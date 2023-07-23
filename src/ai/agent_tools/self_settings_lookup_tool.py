import json
from ai.agent_tools.utilities.abstract_tool import AbstractTool
from ai.agent_tools.utilities.registered_settings import RegisteredSettings


class SelfSettingsLookupTool(AbstractTool):
    def configure(
        self,
        registered_settings: RegisteredSettings,
        memory=None,
        override_llm=None,
        json_args=None,
    ) -> None:
        """settings should be a dictionary of settings, where the key is the name of the setting, and the value is the setting itself"""
        if registered_settings is None:
            raise Exception("SelfSettingsTool requires settings to be passed in")

        self.registered_settings = registered_settings

    def run(self, query: str) -> str:
        # Return a list of the settings and their values
        return json.dumps(self.registered_settings.get_settings())
