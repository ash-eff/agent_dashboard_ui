import json
import os
from PyQt5.QtCore import QUrl, QSize, Qt
from PyQt5.QtGui import QDesktopServices

from pytz import timezone

from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QLabel,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QGroupBox,
)

from datetime import datetime

from link_window import LinkWindow

from user_settings_window import SettingsWindow

from helper_classes import UIComponents as uic
from config import data_dir

class DashboardWindow(QWidget):
    def __init__(self, main, user_settings, parent=None):
        super().__init__(parent)
        self.user_settings = user_settings
        self.links_file = os.path.join(data_dir, 'links.json')
        self.main = main
        self.initUI()
        self.hide()

    def initUI(self):
        # Create all widgets
        self.main_layout = QVBoxLayout()
        self.lower_layout = QHBoxLayout()
        self.upper_layout = QHBoxLayout()
        self.title_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.settings_button_layout = QHBoxLayout()
        self.add_button_layout = QHBoxLayout()
        self.user_greet_label = QLabel(self)
        self.your_time_label = QLabel(self)
        self.your_time = QLabel(self)
        self.cai_time_label = QLabel(self)
        self.cai_time = QLabel(self)
        self.texas_time_label = QLabel(self)
        self.texas_time = QLabel(self)
        self.upper_group = QGroupBox(self)
        self.left_group = QGroupBox(self)
        self.right_group = QGroupBox(self)      
        self.timer = QTimer(self)
        self.spacer = QWidget()
        self.settings_button = QPushButton('Settings', self)
        self.link_label = QLabel('Important Links:', self)
        self.links = QListWidget(self)
        self.add_link_btn = QPushButton('Add Link', self)

        # Set up widget properties
        self.left_group.setFixedWidth(200)
        self.your_time_label.setText('Your Time')
        self.cai_time_label.setText('CAI Time:')
        self.texas_time_label.setText('Texas Time:')
        self.spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.links.setFocusPolicy(Qt.NoFocus)
        self.settings_button.setFixedSize(self.main.btn_x_size + 15, self.main.btn_y_size * 2)
        self.add_link_btn.setFixedSize(self.main.btn_x_size + 15, self.main.btn_y_size * 2)
        self.links.setDragDropMode(QListWidget.InternalMove)

        # Set up layouts
        self.main_layout.addLayout(self.upper_layout)
        self.main_layout.addLayout(self.lower_layout)
        self.upper_group.setLayout(self.title_layout)
        self.left_group.setLayout(self.left_layout)
        self.right_group.setLayout(self.right_layout)
        self.setLayout(self.main_layout)

        # Add widgets to layouts
        self.upper_layout.addWidget(self.upper_group)
        self.title_layout.addStretch(1)
        self.title_layout.addWidget(self.user_greet_label)
        self.title_layout.addStretch(1)
        self.lower_layout.addWidget(self.left_group)
        self.lower_layout.addWidget(self.right_group)
        self.left_layout.addWidget(uic.create_line(self))
        self.left_layout.addWidget(self.cai_time_label)
        self.left_layout.addWidget(self.cai_time)
        self.left_layout.addWidget(uic.create_line(self))
        self.left_layout.addWidget(self.your_time_label)
        self.left_layout.addWidget(self.your_time)
        self.left_layout.addWidget(uic.create_line(self))
        self.left_layout.addWidget(self.texas_time_label)
        self.left_layout.addWidget(self.texas_time)
        self.left_layout.addWidget(uic.create_line(self))
        self.left_layout.addWidget(self.spacer)
        self.settings_button_layout.addWidget(self.settings_button)
        self.left_layout.addLayout(self.settings_button_layout)
        self.right_layout.addWidget(self.link_label)
        self.right_layout.addWidget(self.links)
        self.add_button_layout.setAlignment(Qt.AlignRight)
        self.add_button_layout.addWidget(self.add_link_btn)
        self.right_layout.addLayout(self.add_button_layout)

        # Connect signals
        self.timer.timeout.connect(self.update_time)
        self.settings_button.clicked.connect(self.open_settings)
        self.add_link_btn.clicked.connect(lambda: self.open_link_window('add', ''))
        self.links.itemClicked.connect(self.open_link)
        self.apply_user_settings()
        self.timer.start(1000)

    def showEvent(self, event):
        self.update_time()  
        self.load_links()
        if self.user_settings.get_setting('username') == '':
            QTimer.singleShot(100, self.show_message_box)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.save_links_to_file()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.save_links_to_file()

    def show_message_box(self):
        confirmation = QMessageBox.question(self, 'Update Settings', 'Please update your settings before using this app for the first time.', QMessageBox.Ok)
        if confirmation == QMessageBox.Ok:
            self.open_settings()

    def update_time(self):
        format = '%I:%M:%S %p'

        user_time_zone = self.user_settings.get_current_timezone()
        if user_time_zone != '':
            current_tz = timezone(user_time_zone)
            current_time = datetime.now(current_tz).strftime(format)
        else:
            current_time = 'Please update settings to see your time zone.'

        cai_tz = timezone('US/Eastern')
        cai_time = datetime.now(cai_tz).strftime(format)

        texas_tz = timezone('US/Central')
        texas_time = datetime.now(texas_tz).strftime(format)

        self.your_time.setText(current_time)
        self.cai_time.setText(cai_time)
        self.texas_time.setText(texas_time)

    def open_link_window(self, mode, link_name):
        self.link_window = LinkWindow(mode, link_name, self)
        self.link_window.show()

    def load_links(self):
        self.links.clear()
        try:
            with open(self.links_file, 'r') as file:
                links = json.load(file)
                for link in links:
                    item_layout = QHBoxLayout()
                    link_label = QLabel(link['link_name'])
                    link_label.setObjectName('link_label')
                    link_label.setEnabled(False)
                    item_layout.addWidget(link_label)
                    edit_button = QPushButton('Edit')
                    edit_button.setFixedWidth(40)
                    edit_button.setFixedHeight(40)
                    edit_button.clicked.connect(lambda: self.open_link_window('edit', link['link_name']))
                    item_layout.addWidget(edit_button)
                    delete_button = QPushButton('X')
                    delete_button.setObjectName('warning')
                    delete_button.setFixedWidth(40)
                    delete_button.setFixedHeight(40)
                    delete_button.clicked.connect(lambda: self.open_link_window('delete', link['link_name']))
                    item_layout.addWidget(delete_button)
                    widget = QWidget()
                    widget.setObjectName('link_widget')
                    widget.setLayout(item_layout)
                    widget.setMinimumSize(QSize(widget.width(), 60))
                    item = QListWidgetItem(link['link_name'])
                    item.setSizeHint(widget.sizeHint())
                    self.links.addItem(item)
                    self.links.setItemWidget(item, widget)
            
        except (FileNotFoundError, json.JSONDecodeError):
            default_links = []
            with open(self.links_file, 'w') as file:
                json.dump(default_links, file, indent=4)

    def open_link(self, item):
        link_name = item.text()
        with open(self.links_file, 'r') as file:
            links = json.load(file)
            for link in links:
                if link['link_name'] == link_name:
                    url = link['link_url']
                    if not url.startswith('http://') and not url.startswith('https://'):
                        url = 'http://' + url
                    QDesktopServices.openUrl(QUrl(url))
                    break

    def open_settings(self):
        self.settings_window = SettingsWindow(self.main, self.user_settings, self.main.dark_mode_stylesheet, self.main.light_mode_stylesheet)
        self.settings_window.show()

    def apply_user_settings(self):
        self.user_greet_label.setText(f'Welcome to the Agent Dashboard, {self.user_settings.get_setting("username")}')
        self.update_time()

    def save_links_to_file(self):
        with open(self.links_file, 'r') as file:
            links = json.load(file)
        link_names = [self.links.item(i).text() for i in range(self.links.count())]
        new_json = []
        for name in link_names:
            if name != '':
                for link in links:
                    if link['link_name'] == name:
                        new_json.append(link)

        with open(self.links_file, 'w') as file:
            json.dump(new_json, file, indent=4)
