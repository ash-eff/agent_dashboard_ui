from pytz import timezone

from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QSizePolicy,
    QGroupBox,
    QFrame
)

from datetime import datetime

class DashboardWindow(QWidget):
    def __init__(self, user_settings, parent=None):
        super().__init__(parent)
        self.user_settings = user_settings
        self.initUI()
        #self.hide()

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
        self.links = QTextEdit(self)
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
        self.left_layout.addWidget(self.create_line())
        self.left_layout.addWidget(self.cai_time_label)
        self.left_layout.addWidget(self.cai_time)
        self.left_layout.addWidget(self.create_line())
        self.left_layout.addWidget(self.your_time_label)
        self.left_layout.addWidget(self.your_time)
        self.left_layout.addWidget(self.create_line())
        self.left_layout.addWidget(self.texas_time_label)
        self.left_layout.addWidget(self.texas_time)
        self.left_layout.addWidget(self.create_line())
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
        #self.settings_button.clicked.connect(self.open_settings)

        self.timer.start(1000)

    def showEvent(self, event):
        self.update_time()  

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
    
    def open_settings(self):
        self.user_settings.show()

    def create_line(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line