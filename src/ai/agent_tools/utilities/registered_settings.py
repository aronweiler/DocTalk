class RegisteredSettings:
    # Allow the user to register settings with this class
    # Create a dictionary of settings (name, setting) that we can use later to dynamically set the settings
    
    def __init__(self):
        self.registered_settings = {}
    
    def register_setting(self, name, setting):
        self.registered_settings[name] = setting

    def get_setting(self, name):
        if name in self.registered_settings:
            return self.registered_settings[name]
        else:
            print("Setting not found: " + name)
            return None
    
    def get_settings(self):
        return self.registered_settings
    
    def set_setting(self, name, value):
        # Modify the setting value through the registered settings
        setting = self.get_setting(name)
        if setting is not None:
            setting = value

