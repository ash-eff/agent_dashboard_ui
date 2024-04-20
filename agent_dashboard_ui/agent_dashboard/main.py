import sys

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QMainWindow, 
    QLabel,
    QFrame
)

class AgentDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(0, 600)
        outer_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        bottom_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        self.dashboard_window = DashboardWindow(self)
        self.email_templates_window = EmailTemplatesWindow(self)
        self.format_tool_window = FormatToolWindow(self)
        self.contact_window = ContactWindow(self)

        self.swap_templates(self.dashboard_window)

        self.dashboard_btn = QPushButton('Dashboard', self)
        self.dashboard_btn.setFixedSize(150, 50)
        self.dashboard_btn.clicked.connect(lambda: self.swap_templates(self.dashboard_window))

        self.email_template_btn = QPushButton('Email Templates', self)
        self.email_template_btn.setFixedSize(150, 50)
        self.email_template_btn.clicked.connect(lambda: self.swap_templates(self.email_templates_window))
        
        self.format_btn = QPushButton('Format User Information', self)
        self.format_btn.setFixedSize(150, 50)
        self.format_btn.clicked.connect(lambda: self.swap_templates(self.format_tool_window ))

        self.contact_btn = QPushButton('Contact', self)
        self.contact_btn.setFixedSize(150, 50)
        self.contact_btn.clicked.connect(lambda: self.swap_templates(self.contact_window))

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        horizontal_layout.addWidget(self.dashboard_btn)
        horizontal_layout.addWidget(self.email_template_btn)
        horizontal_layout.addWidget(self.format_btn)
        horizontal_layout.addWidget(self.contact_btn)
        bottom_layout.addLayout(horizontal_layout)

        outer_layout.addLayout(self.top_layout)
        outer_layout.addWidget(line)
        outer_layout.addLayout(bottom_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(outer_layout)
        self.setCentralWidget(central_widget)

    def swap_templates(self, widget):
        for i in reversed(range(self.top_layout.count())):
            old_widget = self.top_layout.itemAt(i).widget()
            old_widget.hide()
            old_widget.setParent(None)
        self.top_layout.addWidget(widget)
        widget.show()


class DashboardWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.hide()

    def showEvent(self, event):
        self.window().setWindowTitle('Dashboard')
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.welcome_label = QLabel("Welcome to the dashboard!", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)

class EmailTemplatesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.hide()

    def showEvent(self, event):
        self.window().setWindowTitle('Email Templates')
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.welcome_label = QLabel("Welcome to the your email templates!", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)

class FormatToolWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.hide()

    def showEvent(self, event):
        self.window().setWindowTitle('Format Tool')
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.welcome_label = QLabel("Welcome to the format tool!", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)

class ContactWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.hide()

    def showEvent(self, event):
        self.window().setWindowTitle('Contact')
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.welcome_label = QLabel("Welcome to the contact page!", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AgentDashboard()
    ex.show()
    sys.exit(app.exec_())