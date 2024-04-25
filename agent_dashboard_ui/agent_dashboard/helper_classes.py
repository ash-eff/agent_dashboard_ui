import json

class ButtonSelectionMixin:
    def __init__(self):
        self.currently_selected_button = None

    def set_button_selected(self, button):
        if self.currently_selected_button is not None:
            self.currently_selected_button.setProperty("class", "")
            self.currently_selected_button.setStyle(self.currently_selected_button.style())
        if button is not None:
            self.currently_selected_button = button
            self.currently_selected_button.setProperty("class", "selected")
            self.currently_selected_button.setStyle(self.currently_selected_button.style())

class UserSettings:
    def __init__(self, settings_file='data/user_settings.json'):
        self.settings_file = settings_file
        self.settings = self.load_settings()

    def load_settings(self):
        with open(self.settings_file, 'r') as file:
            return json.load(file)

    def save_settings(self, new_settings):
        current_settings = self.load_settings()
        current_settings.update(new_settings)
        with open(self.settings_file, 'w') as file:
            json.dump(current_settings, file, indent=4)
        self.settings = current_settings

    def get_settings(self):
        return self.settings

    def get_setting(self, setting_name):
        return self.settings.get(setting_name)

    def set_setting(self, setting_name, setting_value):
        self.settings[setting_name] = setting_value
        self.save_settings(self.settings)

    def get_current_timezone(self):
        TIMEZONE_MAPPING = {
            "Eastern Standard Time": "US/Eastern",
            "Central Standard Time": "US/Central",
            "Pacific Standard Time": "US/Pacific",
            "Mountain Standard Time": "US/Mountain"
        }

        return TIMEZONE_MAPPING[self.settings['user_time_zone']]