from PyQt5.QtWidgets import (
    QWidget, 
    QTextEdit,
    QLineEdit,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QCheckBox,
    QLabel,
    QSizePolicy
)

class SettingsWindow(QWidget):
    def __init__(self, dashboard, user_settings, dark_mode_stylesheet, light_mode_stylesheet, parent=None):
        super().__init__(parent)
        self.dashboard = dashboard
        self.user_settings = user_settings
        self.dark_mode_stylesheet = dark_mode_stylesheet
        self.light_mode_stylesheet = light_mode_stylesheet
        self.setWindowTitle('User Settings')
        self.setMinimumSize(500, 500)
        self.initUI()

    def initUI(self):
        # Create all widgets
        self.layout = QVBoxLayout()
        self.user_time_zone = QComboBox(self)
        self.user_name_label = QLabel('User Name: (First Name, Last Initial)', self)
        self.user_name_field = QLineEdit(self)
        self.time_zone_label = QLabel('Time Zone:', self)
        self.signature_label = QLabel('Email Signature:', self)
        self.signature_box = QTextEdit(self)
        self.dark_mode_checkbox = QCheckBox('Dark Mode', self)
        self.hide_options_checkbox = QCheckBox('Hide Extra Case Options by Default', self)
        self.save_settings_btn = QPushButton('Save Settings', self)
        self.spacer = QWidget()

        # Set up widget properties
        self.spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Set up layouts
        self.setLayout(self.layout)

        # Add widgets to layouts
        self.layout.addWidget(self.user_name_label)
        self.layout.addWidget(self.user_name_field)
        self.layout.addWidget(self.time_zone_label)
        self.layout.addWidget(self.user_time_zone)
        self.layout.addWidget(self.dark_mode_checkbox)
        self.layout.addWidget(self.hide_options_checkbox)
        #self.layout.addWidget(self.spacer)
        self.layout.addWidget(self.signature_label)
        self.layout.addWidget(self.signature_box)
        self.layout.addWidget(self.save_settings_btn)

        # Connect signals
        self.save_settings_btn.clicked.connect(self.save_settings)

    def showEvent(self, event):
        settings = self.user_settings.get_settings()

        for option in settings['time_zone_options']:
            self.user_time_zone.addItem(option)

        if settings['user_time_zone'] != '':
            self.user_time_zone.setCurrentText(settings['user_time_zone'])
        else:
            self.user_time_zone.setCurrentIndex(0)

        self.user_name_field.setText(settings['username'])
        self.signature_box.setText(settings['user_signature'])
        self.dark_mode_checkbox.setChecked(settings['dark_mode'])
        self.hide_options_checkbox.setChecked(settings['hide_case_options'])
        self.user_name_field.setFocus()
    
    def save_settings(self):
        settings = {
            'username': self.user_name_field.text(),
            'user_time_zone': self.user_time_zone.currentText(),
            'user_signature': self.signature_box.toPlainText(),
            'dark_mode': self.dark_mode_checkbox.isChecked(),
            'hide_case_options': self.hide_options_checkbox.isChecked()
        }

        self.user_settings.save_settings(settings)
        self.dashboard.apply_style_settings()
        self.dashboard.dashboard_window.apply_user_settings()
        self.close()

    def get_user_name(self):
        return self.user_settings.get_setting('username')