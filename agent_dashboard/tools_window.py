import os

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QPushButton,
    QHBoxLayout,
    QGroupBox,
    QSizePolicy,
)

from email_template_tool import EmailTemplateBuilderTool
from district_finder_tool import DistrictFinderTool
from user_info_format_tool import UserInfoFormatTool

from config import data_dir

class ToolsWindow(QWidget):
    def __init__(self, main, user_setting, parent=None):
        super().__init__(parent)
        self.user_settings = user_setting
        self.email_tool = EmailTemplateBuilderTool(self)
        self.district_tool = DistrictFinderTool(self)
        self.user_info_tool = UserInfoFormatTool(self)
        self.main = main
        self.domains_file = os.path.join(data_dir, 'domains.json')
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
        self.format_user_btn = QPushButton('Format User Information', self)
        self.email_template_btn = QPushButton('Email Template Creator', self)

        # Set up widget properties
        self.district_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.format_user_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.email_template_btn.setFixedSize(self.btn_x_size, self.btn_y_size)
        self.email_template_btn.setEnabled(False)
        self.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.right_side_group.setStyleSheet("QGroupBox { padding: 10px; }")

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
        self.button_holder_layout.addWidget(self.email_template_btn)
        self.left_layout.addLayout(self.button_holder_layout)
        self.left_layout.addWidget(self.spacer)

        self.outer_layout.setStretch(0,1)
        self.outer_layout.setStretch(1,3)

        #connect signals
        self.district_btn.clicked.connect(lambda: self.swap_templates(self.district_tool))
        self.format_user_btn.clicked.connect(lambda: self.swap_templates(self.user_info_tool))
        self.email_template_btn.clicked.connect(lambda: self.swap_templates(self.email_tool))

    def swap_templates(self, widget):
        for i in reversed(range(self.right_layout.count())):
            old_widget = self.right_layout.itemAt(i).widget()
            old_widget.hide()
            old_widget.setParent(None)
        self.right_layout.addWidget(widget)
        widget.show()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()