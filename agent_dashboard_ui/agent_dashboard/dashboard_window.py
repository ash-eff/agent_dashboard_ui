from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QLabel,
)

from datetime import datetime

class DashboardWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.hide()

        self.welcome_label = QLabel("Welcome to the agent dashboard!", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)

        self.time_label = QLabel(self)
        self.layout.addWidget(self.time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

    def showEvent(self, event):
        self.update_time()  

    def update_time(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.time_label.setText('Current time: ' + current_time)
