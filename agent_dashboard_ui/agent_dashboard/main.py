import logging
import sys
import os

from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QMainWindow, 
    QMessageBox,
    QFrame,
)

from helper_classes import ButtonSelectionMixin, UserSettings
from config import data_dir, style_dir

import dashboard_window as dash_w
import case_notes_window as case_w
import email_templates_window as email_w
import tools_window as tools_w
import contact_window as cont_w
import personal_notes_window as pers_w

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
    filename='crash_report.log',
    filemode='w'
)

# Set up the global exception handler
def handle_uncaught_exceptions(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    error_msg = QMessageBox()
    error_msg.setWindowTitle("Error")
    error_msg.setText("An uncaught exception occurred. Please check the error logs.")
    error_msg.setIcon(QMessageBox.Critical)

    error_msg.exec_()

if getattr(sys, 'frozen', False):
    sys.excepthook = handle_uncaught_exceptions

class AgentDashboard(QMainWindow, ButtonSelectionMixin):
    def __init__(self):
        super().__init__()
        self.dark_mode_stylesheet = None
        self.light_mode_stylesheet = None
        self.load_stylesheets()
        self.user_settings = UserSettings(os.path.join(data_dir, 'user_settings.json'))
        self.currently_selected_button = None
        self.initUI()

    def initUI(self):
        self.resize(1200, 900)
        self.btn_x_size = 150
        self.btn_y_size = 30
        outer_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        horizontal_layout = QHBoxLayout()

        self.dashboard_window = dash_w.DashboardWindow(self, self.user_settings)
        self.case_notes_window = case_w.CaseNotesWindow(self)
        self.email_templates_window = email_w.EmailTemplatesWindow(self, self.user_settings)
        self.tools_window = tools_w.ToolsWindow(self, self.user_settings)
        self.contact_window = cont_w.ContactWindow(self)
        self.personal_notes_window = pers_w.PersonalNotesWindow(self)

        self.dashboard_btn = QPushButton('Dashboard', self)
        self.dashboard_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.dashboard_btn.clicked.connect(lambda: self.swap_templates(self.dashboard_window, 'Agent Dashboard')) 

        self.case_notes_bts = QPushButton('Case Notes', self)
        self.case_notes_bts.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.case_notes_bts.clicked.connect(lambda: self.swap_templates(self.case_notes_window, 'Agent Dashboard - Case Notes'))

        self.email_template_btn = QPushButton('Email Templates', self)
        self.email_template_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.email_template_btn.clicked.connect(lambda: self.swap_templates(self.email_templates_window, 'Agent Dashboard - Email Templates'))
        
        self.tools_btn = QPushButton('Tools', self)
        self.tools_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.tools_btn.clicked.connect(lambda: self.swap_templates(self.tools_window, 'Agent Dashboard - Tools'))

        self.contact_btn = QPushButton('Contact', self)
        self.contact_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.contact_btn.clicked.connect(lambda: self.swap_templates(self.contact_window, 'Agent Dashboard - Contact'))

        self.personal_notes_btn = QPushButton('Personal Notes', self)
        self.personal_notes_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.personal_notes_btn.clicked.connect(lambda: self.swap_templates(self.personal_notes_window, 'Agent Dashboard - Personal Notes'))

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        horizontal_layout.addWidget(self.dashboard_btn)
        horizontal_layout.addWidget(self.case_notes_bts)
        horizontal_layout.addWidget(self.personal_notes_btn)
        horizontal_layout.addWidget(self.email_template_btn)
        horizontal_layout.addWidget(self.tools_btn)
        horizontal_layout.addWidget(self.contact_btn)
        button_layout.addLayout(horizontal_layout)
        
        outer_layout.addLayout(button_layout)
        outer_layout.addWidget(line)
        outer_layout.addLayout(self.top_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(outer_layout)
        self.setCentralWidget(central_widget)
        self.apply_style_settings()

    def showEvent(self, event):
        self.swap_templates(self.dashboard_window, 'Agent Dashboard')
        self.set_button_selected(self.dashboard_btn)   

    def show_status(self, message, time):
        self.statusBar().showMessage(message, time)

    def load_stylesheets(self):
        dark_mode_path = os.path.join(style_dir, 'dark_mode.css')
        light_mode_path = os.path.join(style_dir, 'light_mode.css')
        with open(dark_mode_path, 'r') as f:
            self.dark_mode_stylesheet = f.read()
        with open(light_mode_path, 'r') as f:
            self.light_mode_stylesheet = f.read()

    def swap_templates(self, widget, title):
        self.set_button_selected(self.sender())
        for i in reversed(range(self.top_layout.count())):
            old_widget = self.top_layout.itemAt(i).widget()
            old_widget.hide()
            old_widget.setParent(None)
        self.top_layout.addWidget(widget)
        widget.show()
        self.setWindowTitle(title)

    def apply_style_settings(self):
        settings = self.user_settings.settings
        if settings['dark_mode']:
            QApplication.instance().setStyleSheet(self.dark_mode_stylesheet)
        else:
            QApplication.instance().setStyleSheet(self.light_mode_stylesheet)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = AgentDashboard()
    ex.show()
    sys.exit(app.exec_())