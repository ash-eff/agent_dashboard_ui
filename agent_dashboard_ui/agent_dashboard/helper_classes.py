import json
import os
from PyQt5.QtWidgets import QFrame

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
    def __init__(self, settings_file):
        self.settings_file = settings_file
        if not os.path.isfile(self.settings_file) or os.path.getsize(self.settings_file) == 0:
            default_settings = {
                "username": "",
                "user_time_zone": "Eastern Standard Time",
                "user_signature": "",
                "dark_mode": False,
                "time_zone_options": [
                    "Eastern Standard Time",
                    "Central Standard Time",
                    "Pacific Standard Time",
                    "Mountain Standard Time"
                ],
            }
            with open(self.settings_file, 'w') as file:
                json.dump(default_settings, file, indent=4)
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
    
class UIComponents:
    def create_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line