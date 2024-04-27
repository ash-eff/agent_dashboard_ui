import json
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
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QSizePolicy,
    QGroupBox,
)

from datetime import datetime

from user_settings_window import SettingsWindow

from helper_classes import UIComponents as uic

class DashboardWindow(QWidget):
    def __init__(self, dashboard, user_settings, parent=None):
        super().__init__(parent)
        self.user_settings = user_settings
        self.links_file = 'data/links.json'
        self.dashboard = dashboard
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
        self.upper_group = QGroupBox(self)
        self.left_group = QGroupBox(self)
        self.right_group = QGroupBox(self)      
        self.timer = QTimer(self)
        self.user_greet_label = QLabel(f'Welcome to the Agent Dashboard, {self.user_settings.get_setting("username")}', self)
        self.your_time_label = QLabel(self)
        self.your_time = QLabel(self)
        self.cai_time_label = QLabel(self)
        self.cai_time = QLabel(self)
        self.texas_time_label = QLabel(self)
        self.texas_time = QLabel(self)
        self.spacer = QWidget()
        self.settings_button = QPushButton('Settings', self)
        self.link_label = QLabel('Important Links:', self)
        self.links = QListWidget(self)
        self.add_link_name_label = QLabel('Link Name:', self)
        self.add_link_name = QLineEdit(self)
        self.add_link_url_label = QLabel('Link URL:', self)
        self.add_link_url = QLineEdit(self)
        self.add_link_btn = QPushButton('Add Link', self)

        # Set up widget properties
        self.left_group.setFixedWidth(200)
        self.your_time_label.setText('Your Time')
        self.cai_time_label.setText('CAI Time:')
        self.texas_time_label.setText('Texas Time:')
        self.spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.links.setFocusPolicy(Qt.NoFocus)

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
        self.left_layout.addWidget(self.settings_button)
        self.right_layout.addWidget(self.link_label)
        self.right_layout.addWidget(self.links)
        self.right_layout.addWidget(self.add_link_name_label)
        self.right_layout.addWidget(self.add_link_name)
        self.right_layout.addWidget(self.add_link_url_label)
        self.right_layout.addWidget(self.add_link_url)
        self.right_layout.addWidget(self.add_link_btn)

        # Connect signals
        self.timer.timeout.connect(self.update_time)
        self.add_link_btn.clicked.connect(self.add_link)
        self.settings_button.clicked.connect(self.open_settings)
        self.links.itemClicked.connect(self.open_link)

        self.timer.start(1000)

    def showEvent(self, event):
        self.update_time()  
        self.load_links()

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
    
    def add_link(self):
        link_name = self.add_link_name.text()
        link_url = self.add_link_url.text()
        if link_name and link_url:
            new_link = {
                'link_name': link_name,
                'link_url': link_url
            }

            with open(self.links_file, 'r') as file:
                try:
                    link = json.load(file)
                except json.JSONDecodeError:
                    link = []

            link.append(new_link)

            with open(self.links_file, 'w') as file:
                json.dump(link, file, indent=4)

        self.load_links()

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
                    edit_button.setFixedWidth(80)
                    edit_button.setFixedHeight(80)
                    edit_button.clicked.connect(lambda: self.edit_link(link['link_name']))
                    item_layout.addWidget(edit_button)
                    delete_button = QPushButton('Delete')
                    delete_button.setFixedWidth(80)
                    delete_button.setFixedHeight(80)
                    delete_button.clicked.connect(lambda: self.delete_link(link['link_name']))
                    item_layout.addWidget(delete_button)
                    widget = QWidget()
                    widget.setObjectName('link_widget')
                    widget.setLayout(item_layout)
                    widget.setMinimumSize(QSize(widget.width(), 100))
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
        self.settings_window = SettingsWindow(self.dashboard, self.user_settings, self.dashboard.dark_mode_stylesheet, self.dashboard.light_mode_stylesheet)
        self.settings_window.show()