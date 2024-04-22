from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QLabel,
)

class ContactWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.hide()

    def showEvent(self, event):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.welcome_label = QLabel("Contact and Credits", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.welcome_label)