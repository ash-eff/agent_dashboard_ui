import json
import re

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QHBoxLayout,
    QMessageBox,
    QGroupBox,
    QSizePolicy,
    QApplication,
    QFormLayout,
    QSpacerItem
)

class FormatToolsWindow(QWidget):
    def __init__(self, main, user_setting, parent=None):
            super().__init__(parent)
            self.user_settings = user_setting
            self.main = main
            self.domains_file = main.resource_path('data/domains.json')
            self.btn_x_size = 250
            self.btn_y_size = 75
            self.currently_selected_button = None
            self.ititUI()
            self.hide()

    def ititUI(self):        
        # Create all widgets
        self.main_layout = QVBoxLayout()
        self.outer_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.right_side_group = QGroupBox()
        self.left_side_group = QGroupBox()
        self.button_holder_layout = QVBoxLayout()
        self.spacer = QWidget()

        self.district_btn = QPushButton('District by Email', self)
        self.email_input = QLineEdit(self)
        self.get_district_btn = QPushButton('Get District', self)
        self.district_output = QLabel('', self)
        self.district_irn_label = QLabel('', self)

        self.format_user_btn = QPushButton('Format User Information', self)
        self.user_information_input = QTextEdit(self)
        self.user_information_output = QTextEdit(self)
        self.format_btn = QPushButton('Format', self)
        self.copy_btn = QPushButton('Copy', self)

        # Set up widget properties
        self.district_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.format_user_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_side_group.setStyleSheet("QGroupBox { padding: 10px; }")
        self.user_information_output.setReadOnly(True)

        # Set up layouts
        self.main_layout.addLayout(self.outer_layout)
        self.left_side_group.setLayout(self.left_layout)
        self.right_side_group.setLayout(self.right_layout)

        self.setLayout(self.main_layout)

        # Add widgets to layouts
        self.outer_layout.addWidget(self.left_side_group)
        self.outer_layout.addWidget(self.right_side_group)
        self.button_holder_layout.addWidget(self.district_btn)
        self.button_holder_layout.addWidget(self.format_user_btn)
        self.left_layout.addLayout(self.button_holder_layout)
        self.left_layout.addWidget(self.spacer)

        self.outer_layout.setStretch(0,1)
        self.outer_layout.setStretch(1,3)

        #connect signals
        self.district_btn.clicked.connect(self.show_district_by_email_widget)
        self.get_district_btn.clicked.connect(self.fetch_district)
        self.format_user_btn.clicked.connect(self.show_customer_information_widget)
        self.format_btn.clicked.connect(self.format_customer_information)
        self.copy_btn.clicked.connect(self.copy_user_information)

    def show_district_by_email_widget(self):
        self.clear_layout(self.right_layout)
        self.email_input.clear()
        self.district_output.clear()
        self.district_irn_label.clear()

        form_layout = QFormLayout()
        form_output_layout = QFormLayout()

        form_layout.addRow('User\'s Email:', self.email_input)
        form_output_layout.addRow('District:', self.district_output)
        form_output_layout.addRow('IRN:', self.district_irn_label)

        form_layout.addRow(self.get_district_btn)

        box_widget = QWidget()
        box_widget.setLayout(form_layout)
        box_widget.setObjectName("box_widget")

        output_boxwidget = QWidget()
        output_boxwidget.setLayout(form_output_layout)
        output_boxwidget.setObjectName("box_widget")
        output_boxwidget.hide()

        box_widget.setMinimumSize(int(QApplication.desktop().width() / 4), box_widget.sizeHint().height())
        output_boxwidget.setMinimumSize(int(QApplication.desktop().width() / 4), output_boxwidget.sizeHint().height())

        self.right_layout.addWidget(box_widget, alignment=Qt.AlignCenter)
        self.right_layout.addWidget(output_boxwidget, alignment=Qt.AlignCenter)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.right_layout.addItem(spacer)
        self.get_district_btn.clicked.connect(output_boxwidget.show)

    def show_customer_information_widget(self):
        self.clear_layout(self.right_layout)
        self.user_information_input.clear()
        self.user_information_output.clear()

        form_layout = QVBoxLayout()
        form_output_layout = QVBoxLayout()
        form_layout.addWidget(self.user_information_input)
        form_layout.addWidget(self.format_btn)
        form_output_layout.addWidget(self.user_information_output)
        form_output_layout.addWidget(self.copy_btn)

        box_widget = QWidget()
        box_widget.setLayout(form_layout)
        box_widget.setObjectName("box_widget")

        output_boxwidget = QWidget()
        output_boxwidget.setLayout(form_output_layout)
        output_boxwidget.setObjectName("box_widget")
        output_boxwidget.hide()

        box_widget.setMinimumSize(int(QApplication.desktop().width() / 4), form_layout.sizeHint().height())
        output_boxwidget.setMinimumSize(int(QApplication.desktop().width() / 4), form_layout.sizeHint().height())

        self.right_layout.addWidget(box_widget, alignment=Qt.AlignCenter)
        self.right_layout.addWidget(output_boxwidget, alignment=Qt.AlignCenter)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.right_layout.addItem(spacer)
        self.format_btn.clicked.connect(output_boxwidget.show)

    def fetch_district(self):
        try:
            with open(self.domains_file, 'r') as file:
                domains = json.load(file)
        except FileNotFoundError:
            QMessageBox.critical(self, 'Error', 'Domains file not found. Contact your administrator.')
            return
        
        email_domain = self.email_input.text().split('@')[-1]

        if not email_domain:
            QMessageBox.critical(self, 'Error', 'Please enter a valid email address.')
            return

        for domain in domains:
            if email_domain == domain['Domain']:
                self.district_output.setText(domain['Organization Name'])
                self.district_irn_label.setText(domain['District IRN'])
                return  
             
        else:
            QMessageBox.warning(self, 'Warning', 'Match not found.')
            return
        
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
        self.main.show_status('Email copied to clipboard', 5000)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()