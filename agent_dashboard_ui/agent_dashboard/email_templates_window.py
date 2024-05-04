import json
import os

from PyQt5.QtWidgets import (
    QWidget, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QTextEdit,
    QLabel,
    QComboBox,
    QLineEdit,
    QFormLayout,
    QGroupBox,
    QMessageBox,
    QApplication,
    QSizePolicy,
    QScrollArea
)

from helper_classes import ButtonSelectionMixin
from config import data_dir

class EmailTemplatesWindow(QWidget, ButtonSelectionMixin):
    def __init__(self, main, user_setting, parent=None):
        super().__init__(parent)
        self.user_settings = user_setting
        self.email_templates_file = os.path.join(data_dir, 'email_templates.json')
        self.main = main
        self.btn_x_size = 250
        self.btn_y_size = 75
        self.current_template = None
        self.currently_selected_button = None
        self.ititUI()
        self.hide()

    def ititUI(self):        
        # Create all widgets
        self.main_layout = QVBoxLayout()
        self.outer_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_layout = QVBoxLayout()
        self.upper_right_side_layout = QHBoxLayout()
        self.lower_right_side_layout = QHBoxLayout()
        self.scroll_widget = QWidget()
        self.options_field = QFormLayout()
        self.template_output = QTextEdit(self)
        self.right_side_group = QGroupBox()
        self.left_side_group = QGroupBox()
        self.button_holder_layout = QHBoxLayout()
        self.generate_btn = QPushButton('Generate Email', self)
        self.copy_btn = QPushButton('Copy Email', self)
        self.clear_fields_btn = QPushButton('Clear Fields', self)

        # Set up widget properties
        self.template_output.setReadOnly(True)
        self.generate_btn.setFixedSize(self.main.btn_x_size + 15, self.main.btn_y_size)
        self.generate_btn.hide()
        self.copy_btn.setFixedSize(self.main.btn_x_size + 15, self.main.btn_y_size)
        self.copy_btn.hide()
        self.clear_fields_btn.setFixedSize(self.main.btn_x_size + 15, self.main.btn_y_size)
        self.clear_fields_btn.hide()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(300)

        # Set up layouts
        self.main_layout.addLayout(self.outer_layout)
        self.right_layout.addLayout(self.upper_right_side_layout)
        self.right_layout.addLayout(self.button_holder_layout)
        self.right_layout.addLayout(self.lower_right_side_layout)
        self.upper_right_side_layout.addLayout(self.options_field)
        self.left_side_group.setLayout(self.left_layout)
        self.right_side_group.setLayout(self.right_layout)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.setLayout(self.main_layout)

        # Add widgets to layouts
        self.button_holder_layout.addWidget(self.generate_btn)
        self.button_holder_layout.addWidget(self.copy_btn)
        self.button_holder_layout.addWidget(self.clear_fields_btn)
        self.lower_right_side_layout.addWidget(self.template_output)
        self.outer_layout.addWidget(self.left_side_group)
        self.outer_layout.addWidget(self.right_side_group)

        self.email_templates = self.get_email_templates()
        if self.email_templates != {}:
            for template in self.email_templates:
                template_btn = QPushButton(template.get('title'), self)
                template_btn.setFixedSize(self.btn_x_size, self.btn_y_size)

                template_btn.template_data = template

                template_btn.clicked.connect(self.on_template_btn_clicked)

                self.scroll_layout.addWidget(template_btn)

            self.left_layout.addWidget(self.scroll_area)
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.scroll_layout.addWidget(spacer)

        self.outer_layout.setStretch(0,1)
        self.outer_layout.setStretch(1,3)

        #connect signals
        self.generate_btn.clicked.connect(self.populate_email_from_template)
        self.copy_btn.clicked.connect(self.copy_template)
        self.clear_fields_btn.clicked.connect(self.clear_fields)

    def get_email_templates(self):
        try:
            with open(self.email_templates_file, 'r') as file:
                email_templates = json.load(file)
        except FileNotFoundError:
            email_templates = {}

        return email_templates

    def on_template_btn_clicked(self):
        self.clear_fields()
        button = self.sender()
        self.set_button_selected(button)

        template_data = button.template_data
        
        while self.options_field.count():
            item = self.options_field.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for option in template_data['options']:
            label = QLabel(option['name'])

            if option['type'] == 'dropdown':
                dropdown = QComboBox()
                dropdown.addItems(option['values'])
                self.options_field.addRow(label,dropdown)
            elif option['type'] == 'input':
                input_field = QLineEdit()
                self.options_field.addRow(label, input_field)
            elif option['type'] == 'text':
                text_field = QTextEdit()
                self.options_field.addRow(label, text_field)
        
        self.generate_btn.show()
        self.copy_btn.show()
        self.clear_fields_btn.show()
        self.current_template = template_data

    def populate_email_from_template(self):
        template_text = self.current_template['text']

        values = {}

        for i in range(0, self.options_field.count(), 2):
            label_widget = self.options_field.itemAt(i).widget()
            value_widget = self.options_field.itemAt(i + 1).widget()
            
            label = label_widget.text()

            if isinstance(value_widget, QComboBox):
                value = value_widget.currentText()
            elif isinstance(value_widget, QLineEdit):
                value = value_widget.text()
            elif isinstance(value_widget, QTextEdit):
                value = value_widget.toPlainText()

            if not value:
                QMessageBox.warning(self, 'Error', 'Please fill out all fields before generating email.')        
                return
            
            values[label] = value

        template_text = template_text.format(**values)
        settings = self.user_settings.get_settings()
        agent_name = settings['username']
        signature_text = settings['user_signature']
        
        if signature_text == '':
            QMessageBox.question(self, 'No Signature', 'You forgot to set a signature in your settings. You will need to adjust your email before sending it.', QMessageBox.Ok)

        if agent_name == '':
            QMessageBox.question(self, 'No Name', 'You forgot to set your name in your settings. You will need to adjust your email before sending it.', QMessageBox.Ok)

        self.template_output.setPlainText(template_text + agent_name + signature_text)

    def copy_template(self):
        if self.template_output.toPlainText() == '':
            self.main.show_status('No email to copy', 5000)
            return
        
        text = self.template_output.toPlainText()

        clipboard = QApplication.clipboard()

        clipboard.setText(text)
        self.main.show_status('Email copied to clipboard', 5000)

    def clear_fields(self):
        self.template_output.clear()
        for i in range(0, self.options_field.count(), 2):
            value_widget = self.options_field.itemAt(i + 1).widget()
            if isinstance(value_widget, QComboBox):
                value_widget.setCurrentIndex(0)
            elif isinstance(value_widget, QLineEdit):
                value_widget.clear()