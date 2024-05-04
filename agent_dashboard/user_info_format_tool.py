import re

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QPushButton,
    QTextEdit,
    QMessageBox,
    QSizePolicy,
    QApplication,
    QSpacerItem,
)

class UserInfoFormatTool(QWidget):
    def __init__(self, tool_window, parent=None):
        super().__init__()
        self.tool_window = tool_window
        self.initUI()
        self.hide()

    def initUI(self):
        # Create all widgets
        self.layout = QVBoxLayout()
        self.user_information_input = PlainTextPasteQTextEdit()
        self.user_information_output = QTextEdit()
        self.format_btn = QPushButton('Format')
        self.copy_btn = QPushButton('Copy')
        self.form_layout = QVBoxLayout()
        self.form_output_layout = QVBoxLayout()
        self.box_widget = QWidget()
        self.output_boxwidget = QWidget()

        # Set up widget properties
        self.user_information_output.setReadOnly(True)

        # Set up layouts
        self.box_widget.setLayout(self.form_layout)
        self.box_widget.setObjectName("box_widget")
        self.output_boxwidget.setLayout(self.form_output_layout)
        self.output_boxwidget.setObjectName("box_widget")
        self.output_boxwidget.hide()
        self.box_widget.setMinimumSize(int(QApplication.desktop().width() / 4), self.form_layout.sizeHint().height())
        self.output_boxwidget.setMinimumSize(int(QApplication.desktop().width() / 4), self.form_layout.sizeHint().height())

        # Add widgets to layouts
        self.form_layout.addWidget(self.user_information_input)
        self.form_layout.addWidget(self.format_btn)
        self.form_output_layout.addWidget(self.user_information_output)
        self.form_output_layout.addWidget(self.copy_btn)
        self.layout.addWidget(self.box_widget, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.output_boxwidget, alignment=Qt.AlignCenter)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)
        self.setLayout(self.layout)
        self.format_btn.clicked.connect(self.output_boxwidget.show)

        #connect signals
        self.format_btn.clicked.connect(self.format_customer_information)
        self.copy_btn.clicked.connect(self.copy_user_information)

    # def showEvent(self, event):
    #     self.user_information_input.clear()
    #     self.user_information_output.clear()
        
    def format_customer_information(self):
        customer_info = self.user_information_input.toPlainText()
        if not customer_info:
            QMessageBox.critical(self, 'Error', 'Please enter customer information.')
            return
        remove_all_before_name = re.sub(r'.*Close', 'Name:', customer_info, flags=re.DOTALL)
        remove_create_date_and_beyond = re.sub(r'Create Date:.+', 'Case Creation Date:', remove_all_before_name, flags=re.DOTALL)
        remove_customer_id = re.sub(r'\[(.*?)Voice:', 'Voice:', remove_create_date_and_beyond, flags=re.DOTALL)
        remove_alternative = re.sub(r'Alternative:(.*?)Project State:', 'Project State:', remove_customer_id, flags=re.DOTALL)
        remove_region_code = re.sub(r'Region Code:(.*?)Region:', 'Region:', remove_alternative, flags=re.DOTALL)
        remove_fax = re.sub(r'\bFax:\s*', '', remove_region_code)
        clean_results = remove_fax

        customer_info_lines = clean_results.split('\n')
        filtered_lines = [line for line in customer_info_lines if line.strip()]
        words_to_check = ["Name", "Voice", "Email", "Company", "Project State", "Region", "District Code", "District", "School Code", "Case Creation Date:"]
        formatted_customer_info = []
        skip_next = False
        for i in range(len(filtered_lines)):
            if skip_next:
                skip_next = False
                continue

            line = filtered_lines[i].strip()
            if i + 1 < len(filtered_lines) and not any(filtered_lines[i + 1].strip().startswith(word + ':') for word in words_to_check):
                formatted_customer_info.append(f'{line} {filtered_lines[i + 1].strip()}')
                skip_next = True
            else:
                formatted_customer_info.append(line)

        block_of_customer_info = '\n'.join(formatted_customer_info)
        self.user_information_output.setText(block_of_customer_info)
        
    def copy_user_information(self):
        if self.user_information_output.toPlainText() == '':
            self.main.show_status('No email to copy', 5000)
            return
        
        text = self.user_information_output.toPlainText()

        clipboard = QApplication.clipboard()

        clipboard.setText(text)
        self.tool_window.main.show_status('Email copied to clipboard', 5000)

class PlainTextPasteQTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())