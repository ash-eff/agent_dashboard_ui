import json

from PyQt5.QtWidgets import (
    QWidget, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout,
    QTextEdit,
    QLabel,
    QSizePolicy,
    QComboBox,
    QLineEdit,
    QFormLayout,
    QGroupBox,
    QMessageBox,
    QApplication
)

from helper_classes import ButtonSelectionMixin

class EmailTemplatesWindow(QWidget, ButtonSelectionMixin):
    def __init__(self, dashboard, user_setting, parent=None):
        super().__init__(parent)
        self.user_settings = user_setting
        self.email_templates_file = 'data/email_templates.json'
        self.dashboard = dashboard
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
        self.upper_right_side_layout = QHBoxLayout()
        self.lower_right_side_layout = QHBoxLayout()
        self.spacer = QWidget()
        self.options_field = QFormLayout()
        self.template_output = QTextEdit(self)
        self.spacer = QWidget()
        self.right_side_group = QGroupBox()
        self.button_holder_layout = QHBoxLayout()
        self.generate_btn = QPushButton('Generate Email', self)
        self.copy_btn = QPushButton('Copy Email', self)
        self.clear_fields_btn = QPushButton('Clear Fields', self)

        # Set up widget properties
        self.spacer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.template_output.setReadOnly(True)
        self.generate_btn.setFixedSize(self.dashboard.btn_x_size + 15, self.dashboard.btn_y_size)
        self.generate_btn.hide()
        self.copy_btn.setFixedSize(self.dashboard.btn_x_size + 15, self.dashboard.btn_y_size)
        self.copy_btn.hide()
        self.clear_fields_btn.setFixedSize(self.dashboard.btn_x_size + 15, self.dashboard.btn_y_size)
        self.clear_fields_btn.hide()

        # Set up layouts
        self.main_layout.addLayout(self.outer_layout)
        self.outer_layout.addLayout(self.left_layout)
        self.right_layout.addLayout(self.upper_right_side_layout)
        self.right_layout.addLayout(self.button_holder_layout)
        self.right_layout.addLayout(self.lower_right_side_layout)
        self.upper_right_side_layout.addLayout(self.options_field)
        self.right_side_group.setLayout(self.right_layout)
        self.setLayout(self.main_layout)


        # Add widgets to layouts
        self.button_holder_layout.addWidget(self.generate_btn)
        self.button_holder_layout.addWidget(self.copy_btn)
        self.button_holder_layout.addWidget(self.clear_fields_btn)
        self.lower_right_side_layout.addWidget(self.template_output)
        self.outer_layout.addWidget(self.right_side_group)

        self.email_templates = self.get_email_templates()
        if self.email_templates != {}:
            for template in self.email_templates:
                template_btn = QPushButton(template.get('title'), self)
                template_btn.setFixedSize(self.btn_x_size, self.btn_y_size)

                template_btn.template_data = template

                template_btn.clicked.connect(self.on_template_btn_clicked)

                self.left_layout.addWidget(template_btn)

        self.left_layout.addWidget(self.spacer)

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

            if not value:
                QMessageBox.warning(self, 'Error', 'Please fill out all fields before generating email.')        
                return
            
            values[label] = value

        template_text = template_text.format(**values)
        settings = self.user_settings.get_settings()
        user_name = settings['username']
        signature_text = settings['user_signature']

        self.template_output.setPlainText(template_text + user_name + '\n' + signature_text)

    def copy_template(self):
        if self.template_output.toPlainText() == '':
            self.dashboard.show_status('No email to copy', 5000)
            return
        
        text = self.template_output.toPlainText()

        clipboard = QApplication.clipboard()

        clipboard.setText(text)
        self.dashboard.show_status('Email copied to clipboard', 5000)

    def clear_fields(self):
        self.template_output.clear()
        for i in range(0, self.options_field.count(), 2):
            value_widget = self.options_field.itemAt(i + 1).widget()
            if isinstance(value_widget, QComboBox):
                value_widget.setCurrentIndex(0)
            elif isinstance(value_widget, QLineEdit):
                value_widget.clear()