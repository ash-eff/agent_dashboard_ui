import sys

from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QMainWindow, 
    QFrame,
)

import dashboard_window as dash_w
import case_notes_window as case_w
import email_templates_window as email_w
import format_tools_window as format_w
import contact_window as cont_w

class AgentDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Agent Dashboard')
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        outer_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        bottom_layout = QVBoxLayout()
        horizontal_layout = QHBoxLayout()

        self.dashboard_window = dash_w.DashboardWindow(self)
        self.case_notes_window = case_w.CaseNotesWindow(self)
        self.email_templates_window = email_w.EmailTemplatesWindow(self)
        self.format_tool_window = format_w.FormatToolsWindow(self)
        self.contact_window = cont_w.ContactWindow(self)

        self.swap_templates(self.dashboard_window)

        self.dashboard_btn = QPushButton('Dashboard', self)
        self.dashboard_btn.setFixedSize(150, 50)
        self.dashboard_btn.clicked.connect(lambda: self.swap_templates(self.dashboard_window))

        self.case_notes_bts = QPushButton('Case Notes', self)
        self.case_notes_bts.setFixedSize(150, 50)
        self.case_notes_bts.clicked.connect(lambda: self.swap_templates(self.case_notes_window))

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
        horizontal_layout.addWidget(self.case_notes_bts)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AgentDashboard()
    ex.show()
    sys.exit(app.exec_())