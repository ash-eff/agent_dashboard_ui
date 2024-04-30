from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, 
    QTextEdit,
    QVBoxLayout,
    QApplication,
    QMenu,
    QAction,
    QPushButton
)

class EmailTemplateBuilderTool(QWidget):
    def __init__(self, tool_window, parent=None):
        super().__init__(parent)
        self.tool_window = tool_window
        self.initUI()
        self.hide()

    def initUI(self):
        # Create all widgets
        self.email_template = CustomTextEdit(self)
        self.box_layout = QVBoxLayout()
        self.box_layout.addWidget(self.email_template)

        self.setLayout(self.box_layout)

        # Set up widget properties

        # Set up layouts

        # Add widgets to layouts

        # Connect signals

    def add_dropdown_menu(self):
        words = self.email_template.toPlainText().split()
        words.insert(self.email_template.textCursor().position(), 'dropdown')
        self.email_template.setText(' '.join(words))

class CustomTextEdit(QTextEdit):
    def __init__(self, tools_window, parent=None):
        super().__init__(parent)
        self.tools_window = tools_window

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        action1 = QAction('Add Dropdown Menu', self)
        action2 = QAction('Add Input Field', self)
        action3 = QAction('Add Text Field', self)

        context_menu.addAction(action1)
        context_menu.addAction(action2)
        context_menu.addAction(action3)

        action1.triggered.connect(self.tools_window.add_dropdown_menu)

        context_menu.exec_(event.globalPos())
