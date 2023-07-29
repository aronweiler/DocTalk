from enum import Enum
from memory.long_term.database.vector_database import SearchType

class SettingsActionType(Enum):
    list = "list"
    set = "set"

class Setting:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    @staticmethod
    def from_json(json_args):
        return Setting(
            name=json_args["setting_name"],
            value=json_args["setting_value"],
        )

class SettingsAction:
    def __init__(self, action: str, associated_user_email, settings):
        
        if associated_user_email is None:
            raise ValueError("'associated_user_email' is a required field")
        
        try:
            self.settings_action = SettingsActionType[action]
        except:
            raise ValueError(f"settings_action is not valid. settings_action must be either '{SettingsActionType.list}', or '{SettingsActionType.set}'.")

        
        self.associated_user_email = associated_user_email
        self.settings = settings

    # Static method to construct the class from a json object
    @staticmethod
    def from_json(json_args):
        return SettingsAction(
            action=json_args["setting_action"],
            associated_user_email=json_args["associated_user"] if "associated_user" in json_args else None,
            settings = SettingsAction.settings_from_json(json_args["settings"]) if "settings" in json_args else None
        )
    
    @staticmethod
    def settings_from_json(json_settings):
        settings = []
        for setting in json_settings:
            settings.append(Setting.from_json(setting))

        return settings
        