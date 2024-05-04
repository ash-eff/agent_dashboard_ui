from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QWidget, 
    QTextEdit,
    QVBoxLayout,
    QMenu,
    QAction,
    QInputDialog,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QLabel
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
        self.options = QListWidget(self)

        # Set up widget properties

        # Set up layouts
        self.box_layout.addWidget(self.email_template)
        self.box_layout.addWidget(self.options)
        self.setLayout(self.box_layout)

        # Add widgets to layouts

        # Connect signals

    def add_dropdown_menu(self):
        dropdown_name, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter dropdown name:')
        if ok:
            dropdown_items, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter dropdown items separated by comma:')
            if ok:
                dropdown_items = dropdown_items.split(',')
                self.add_option(dropdown_name, dropdown_items)
                words = self.email_template.toPlainText().split()
                words.insert(self.email_template.textCursor().position(), '{' + dropdown_name + '}')
                self.email_template.setText(' '.join(words))

    def add_option(self, option_name, option_items):
        item_layout = QHBoxLayout()
        widget = QWidget()
        widget.setObjectName('link_widget')

        # Create a QLabel with the formatted_option text
        label = QLabel(f"{option_name} : {', '.join(option_items)}")
        item_layout.addWidget(label)
        widget.setLayout(item_layout)
        widget.setMinimumSize(QSize(widget.width(), 60))

        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.options.addItem(item)
        self.options.setItemWidget(item, widget)    

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
