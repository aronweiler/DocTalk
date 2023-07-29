import json
import logging

# For testing
# Add the root path to the python path so we can import the database
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from ai.agent_tools.utilities.abstract_tool import AbstractTool
from ai.agent_tools.settings.settings_tool_configuration import SettingsToolConfiguration
from ai.agent_tools.settings.settings_action import SettingsAction, SettingsActionType

from memory.long_term.database.users import Users
from memory.long_term.models import User

class SettingsTool(AbstractTool):
    def configure(
        self,
        memory=None,
        override_llm=None,
        json_args=None,
    ) -> None:
        self.configuration = SettingsToolConfiguration(json_args)
        self.users = Users(self.configuration.db_env_location)   

    def run(self, query: str) -> str:
        logging.debug("SettingsTool got query: " + query)

        try:
            json_args = json.loads(query)

            # Parse the query
            settings_action = SettingsAction.from_json(json_args)
            
            if settings_action is not None:
                # Return a list of the settings and their values        
                with self.users.session_context(self.users.Session()) as session:
                    user = self.users.find_user_by_email(session, settings_action.associated_user_email, eager_load=[User.user_settings])

                    if user is None:
                        return f"Error: User '{settings_action.associated_user_email}' not found"

                    if settings_action.settings_action == SettingsActionType.list:                        
                        return "The settings I have are: " + ', '.join([f"{setting.setting_name}='{setting.setting_value}'" for setting in user.user_settings])
                                
                    elif settings_action.settings_action == SettingsActionType.set:
                        for setting in settings_action.settings:
                            user.set_setting(setting.name, setting.value)

                        return "Settings updated"
                    else:
                        return "Error: Invalid query, read the tool instructions and try again"
            else:
                return "Error: Invalid query, read the tool instructions and try again"
        
        except Exception as e:
            logging.error(e)            
            return "Error: " + str(e)

# testing
if __name__ == "__main__":
    settings_tool = SettingsTool()
    settings_tool.configure(json_args={"db_env_location": "src/memory/long_term/db.env"})
    print(settings_tool.run("{\"setting_action\": \"list\", \"associated_user\": \"aronweiler@gmail.com\"}"))
    # print(settings_tool.run("{\"setting_action\": \"list\", \"associated_user\": \"gaiaweiler@gmail.com\"}"))
    # print(settings_tool.run("{\"setting_action\": \"list\", \"associated_user\": \"aronweiler@gmail.com\"}"))   
    settings_tool.run("{\"setting_action\": \"set\", \"associated_user\": \"aronweiler@gmail.com\", \"settings\": [{\"setting_name\": \"speech_rate\", \"setting_value\": \"150\"}]}") 
    print(settings_tool.run("{\"setting_action\": \"list\", \"associated_user\": \"aronweiler@gmail.com\"}"))