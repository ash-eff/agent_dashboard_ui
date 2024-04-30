import json

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, 
    QPushButton,
    QLabel,
    QLineEdit,
    QApplication,
    QFormLayout,
    QMessageBox,
    QVBoxLayout,
    QSizePolicy,
    QSpacerItem,
)

class DistrictFinderTool(QWidget):
    def __init__(self, tool_window, parent=None):
        super().__init__()
        self.tool_window = tool_window
        self.initUI()
        self.hide()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.email_input = QLineEdit()
        self.get_district_btn = QPushButton('Get District')
        self.district_output = QLabel('')
        self.district_irn_label = QLabel('')

        self.get_district_btn.clicked.connect(self.fetch_district)
        
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

        self.layout.addWidget(box_widget, alignment=Qt.AlignCenter)
        self.layout.addWidget(output_boxwidget, alignment=Qt.AlignCenter)
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)
        self.setLayout(self.layout)
        self.get_district_btn.clicked.connect(output_boxwidget.show)

    def fetch_district(self):
        try:
            with open(self.tool_window.domains_file, 'r') as file:
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
        
    def clear_data(self):
        self.email_input.clear()
        self.district_output.clear()
        self.district_irn_label.clear()