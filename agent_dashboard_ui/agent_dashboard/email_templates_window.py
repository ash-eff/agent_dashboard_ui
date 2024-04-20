from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, 
    QPushButton, 
    QVBoxLayout,  
    QLabel,
)

class EmailTemplatesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.hide()

    def showEvent(self, event):
        self.window()
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.welcome_label = QLabel("Email Templates", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.template_btn1 = QPushButton('Template 1', self)
        self.template_btn1.setFixedSize(150, 50)
        self.template_btn2 = QPushButton('Template 2', self)
        self.template_btn2.setFixedSize(150, 50)
        self.template_btn3 = QPushButton('Template 3', self)
        self.template_btn3.setFixedSize(150, 50)
        self.layout.addWidget(self.welcome_label)
        self.layout.addWidget(self.template_btn1)
        self.layout.addWidget(self.template_btn2)
        self.layout.addWidget(self.template_btn3) 