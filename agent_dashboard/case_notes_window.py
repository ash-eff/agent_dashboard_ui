import json
import os

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QGroupBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QApplication
)

from note import CaseNote as Note

from helper_classes import ButtonSelectionMixin
from config import data_dir

class CaseNotesWindow(QWidget, ButtonSelectionMixin):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.case_file = os.path.join(data_dir, 'case_notes.json')
        self.main = main
        self.last_note_title = ''
        self.original_note_title = ''
        self.initUI()
        self.hide()

    def initUI(self): 
        # Create all widgets
        self.main_layout = QVBoxLayout()
        self.outer_layout = QHBoxLayout()
        self.note_button_layout = QVBoxLayout()
        self.outer_right_layout = QHBoxLayout()
        self.note_layout = QHBoxLayout()
        self.options_layout = QFormLayout()
        self.options_vertical_layout = QVBoxLayout()
        self.note_button_group = QGroupBox()
        self.outer_right_group = QGroupBox()
        self.note_group = QGroupBox()
        self.options_group = QGroupBox()
        self.scroll_area = QScrollArea(self)
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget = QWidget()
        self.bottom_button_layout = QHBoxLayout()
        self.new_note_btn = QPushButton('New Note', self)      
        self.save_note_btn = QPushButton('Save Note', self)
        self.collapse_options_btn = QPushButton('Collapse Options', self)
        self.purge_notes_btn = QPushButton('Purge Notes', self)
        self.delete_note_btn = QPushButton('Delete Note', self)
        self.copy_note_btn = QPushButton('Copy Notes', self)
        self.copy_note_layout = QVBoxLayout()
        self.copy_note_btn_layout = QHBoxLayout()
        self.copy_option_btn = QPushButton('Copy Options', self)
        self.copy_all_btn = QPushButton('Copy All', self)
        self.copy_btn_layout = QHBoxLayout()
        self.case_notes = PlainTextPasteQTextEdit(self)
        self.case_number_label = QLabel('Case Number')
        self.case_number_line = QLineEdit()
        self.tid_label = QLabel('TID')
        self.tid_line = QLineEdit()
        self.user_name_label = QLabel('User Name')
        self.user_name_line = QLineEdit()
        self.phone_number_label = QLabel('Phone Number')
        self.phone_number_line = QLineEdit()
        self.email_label = QLabel('Email')
        self.email_line = QLineEdit()
        self.role_label = QLabel('Role')
        self.role_line = QLineEdit()
        self.region_label = QLabel('Region')
        self.region_line = QLineEdit()
        self.district_label = QLabel('District')
        self.district_line = QLineEdit()
        self.campus_label = QLabel('Campus')
        self.campus_line = QLineEdit()
        self.tsds_label = QLabel('TSDS')
        self.tsds_line = QLineEdit()
        self.test_name_label = QLabel('Test Name')
        self.test_name_line = QLineEdit()
        self.test_status_label = QLabel('Test Status')
        self.test_status_line = QLineEdit()
        self.session_id_label = QLabel('Session ID')
        self.session_id_line = QLineEdit()
        self.rid_label = QLabel('RID')
        self.rid_line = QLineEdit()
        self.accommodations_label = QLabel('Accommodations')
        self.accommodations_line = QLineEdit()
        self.error_label = QLabel('Error')
        self.error_line = QLineEdit()
        self.option_spacer = QWidget()

        # Set up widget properties
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(190)
        self.collapse_options_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.purge_notes_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.new_note_btn.setFixedHeight(50)
        self.new_note_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.new_note_btn.setObjectName('new_note_btn')
        self.save_note_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.copy_note_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.copy_option_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.copy_all_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.delete_note_btn.setObjectName('warning')
        self.delete_note_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.case_notes.setPlaceholderText('Case Notes')
        self.case_notes.setObjectName('case_note')
        self.note_button_group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.options_layout.setLabelAlignment(Qt.AlignRight)
        self.option_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.purge_notes_btn.setObjectName('warning')

        self.outer_layout.setStretch(0,1)
        self.outer_layout.setStretch(1,4)

        self.note_layout.setStretch(1,2)
        self.note_layout.setStretch(2,2)

        # Set up layouts
        self.main_layout.addLayout(self.outer_layout)
        self.main_layout.addLayout(self.bottom_button_layout)

        self.outer_layout.addWidget(self.note_button_group)
        self.outer_layout.addWidget(self.outer_right_group)

        self.bottom_button_layout.addStretch()
        self.bottom_button_layout.addWidget(self.collapse_options_btn, alignment=Qt.AlignRight)
        self.bottom_button_layout.addWidget(self.purge_notes_btn, alignment=Qt.AlignRight)

        self.outer_right_group.setLayout(self.outer_right_layout)
        self.outer_right_layout.addWidget(self.note_group)
        self.outer_right_layout.addWidget(self.options_group)

        self.copy_note_btn_layout.addStretch()
        self.note_group.setLayout(self.copy_note_layout)
        self.copy_note_layout.addWidget(self.case_notes)
        self.copy_note_layout.addLayout(self.copy_note_btn_layout)
        self.copy_note_btn_layout.addWidget(self.delete_note_btn, alignment=Qt.AlignRight)
        self.copy_note_btn_layout.addWidget(self.save_note_btn, alignment=Qt.AlignRight)
        self.copy_note_btn_layout.addWidget(self.copy_note_btn, alignment=Qt.AlignRight)


        self.options_group.setLayout(self.options_vertical_layout)
        self.options_vertical_layout.addLayout(self.options_layout)
        self.options_vertical_layout.addWidget(self.option_spacer)
        self.options_vertical_layout.addLayout(self.copy_btn_layout)
        self.copy_btn_layout.addWidget(self.copy_all_btn, alignment=Qt.AlignLeft)
        self.copy_btn_layout.addWidget(self.copy_option_btn, alignment=Qt.AlignRight)
        
        self.note_button_group.setLayout(self.note_button_layout)
        self.note_button_layout.addWidget(self.new_note_btn)
        self.note_button_layout.addWidget(self.scroll_area)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        self.options_layout.addRow(self.case_number_label, self.case_number_line)
        self.options_layout.addRow(self.tid_label, self.tid_line)
        self.options_layout.addRow(self.user_name_label, self.user_name_line)
        self.options_layout.addRow(self.phone_number_label, self.phone_number_line)
        self.options_layout.addRow(self.email_label, self.email_line)
        self.options_layout.addRow(self.role_label, self.role_line)
        self.options_layout.addRow(self.region_label, self.region_line)
        self.options_layout.addRow(self.district_label, self.district_line)
        self.options_layout.addRow(self.campus_label, self.campus_line)
        self.options_layout.addRow(self.tsds_label, self.tsds_line)
        self.options_layout.addRow(self.test_name_label, self.test_name_line)
        self.options_layout.addRow(self.test_status_label, self.test_status_line)
        self.options_layout.addRow(self.session_id_label, self.session_id_line)
        self.options_layout.addRow(self.rid_label, self.rid_line)
        self.options_layout.addRow(self.accommodations_label, self.accommodations_line)
        self.options_layout.addRow(self.error_label, self.error_line)

        self.setLayout(self.main_layout)

        #connect signals
        self.new_note_btn.clicked.connect(self.open_blank_note)
        self.save_note_btn.clicked.connect(self.save_note)
        self.delete_note_btn.clicked.connect(self.delete_note)
        self.collapse_options_btn.clicked.connect(self.toggle_options)
        self.purge_notes_btn.clicked.connect(self.purge_notes)
        self.copy_note_btn.clicked.connect(self.copy_notes)
        self.copy_option_btn.clicked.connect(self.copy_options)
        self.copy_all_btn.clicked.connect(self.copy_all)

    def showEvent(self, event):
        self.clear_layout(self.scroll_layout) 
        self.load_note_buttons()
        self.load_last_note()
        if self.main.user_settings.settings['hide_case_options']:
            self.hide_options(True)
        else:
            self.hide_options(False)
        button = self.get_button_from_title(self.last_note_title)
        if button is not None:
            self.set_button_selected(button)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.save_note()
    
    def toggle_options(self):
        if self.options_group.isHidden():
            self.hide_options(False)
        else:
            self.hide_options(True)

    def hide_options(self, is_hidden):
        if is_hidden:
            self.options_group.hide()
            self.collapse_options_btn.setText('Expand Options')
        else:
            self.options_group.show()
            self.collapse_options_btn.setText('Collapse Options')

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
            elif layout.itemAt(i).layout() is not None:
                self.clear_layout(layout.itemAt(i).layout())

    def clear_form_layout(self, form_layout):
        for i in range(form_layout.count()):
            item = form_layout.itemAt(i)
            widget = item.widget()

            if widget is not None:
                if isinstance(widget, (QLineEdit, QTextEdit)):
                    widget.clear()

    def open_blank_note(self):
        self.case_notes.setText('')
        self.last_note_title = ''
        self.original_note_title = ''
        self.clear_form_layout(self.options_layout)

    def open_note(self, note_dict):
        note = Note.from_dict(note_dict)

        self.case_notes.setText(note.notes)
        self.last_note_title = note.title
        self.original_note_title = note.title

        note_dict = note.to_dict()

        for i in range(0, self.options_layout.rowCount()):
            item = self.options_layout.itemAt(i, QFormLayout.LabelRole)

            if item is not None:
                label_widget = item.widget()
                value_widget = self.options_layout.itemAt(i, QFormLayout.FieldRole).widget()

                if label_widget is not None and value_widget is not None:
                    label_text = label_widget.text()

                    if label_text in note_dict:
                        value_widget.setText(str(note_dict[label_text]))
         
    def load_last_note(self):
        try:
            with open(self.case_file, 'r') as file:
                try:
                    notes_dict = json.load(file)
                except json.JSONDecodeError:
                    notes_dict = []
        except FileNotFoundError:
            notes_dict = []

        notes = [Note.from_dict(note) for note in notes_dict]

        if self.last_note_title != '':
            for note in notes:
                if note.title == self.last_note_title:
                    self.original_note_title = note.title
                    self.open_note(note.to_dict())
                    break
            else:
                self.open_blank_note()
        else:
            if notes: 
                first_note = notes[0]
                self.original_note_title = first_note.title
                self.open_note(first_note.to_dict())
            else:
                self.open_blank_note()

    def save_note(self):
        if self.case_notes.toPlainText() == '':
            return
        options = {}
        for i in range(0, self.options_layout.rowCount()):
            label_widget = self.options_layout.itemAt(i, QFormLayout.LabelRole).widget()
            value_widget = self.options_layout.itemAt(i, QFormLayout.FieldRole).widget()

            label = label_widget.text()
            value = value_widget.text()

            options[label] = value

        notes = self.case_notes.toPlainText()
        title = self.last_note_title if self.last_note_title != '' else None

        note = Note(notes, title, **options)
        note_dict = note.to_dict()

        try:
            with open(self.case_file, 'r') as file:
                try:
                    existing_notes = json.load(file)
                except json.JSONDecodeError:
                    existing_notes = []
        except FileNotFoundError:
            existing_notes = []

        new_note_added = False
        for i, existing_note in enumerate(existing_notes):
            if existing_note['title'] == self.original_note_title:
                existing_notes[i] = note_dict
                self.main.show_status('Case updated successfully', 2000)
                break
        else:
            existing_notes.append(note_dict)
            new_note_added = True

        with open(self.case_file, 'w') as file:
            json.dump(existing_notes, file, indent=4)

        self.last_note_title = note_dict['title']
        self.original_note_title = note_dict['title']
        if new_note_added:
            self.main.show_status('Case saved successfully', 2000)
            self.load_note_buttons()

    def load_note_buttons(self):
        button = None
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        try:
            with open(self.case_file, 'r') as file:
                if os.stat(self.case_file).st_size != 0:
                    notes_dict = json.load(file)
                else:
                    notes_dict = []
        except FileNotFoundError:
            notes_dict = []

        notes = [Note.from_dict(note_dict) for note_dict in notes_dict]

        for note in notes:
            if note.title:
                button = QPushButton(note.title)
                button.setFixedSize(150, 50)
                button.note_title = note.title
                button.clicked.connect(self.open_note_from_button)
                self.scroll_layout.addWidget(button)

        if button is not None:
            self.set_button_selected(button)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.scroll_layout.addWidget(spacer)

    def open_note_from_button(self):
        button = self.sender()
        self.save_note()
        self.set_button_selected(button)
        with open(self.case_file, 'r') as file:
            notes_dict = json.load(file)
        note_dict = next((note for note in notes_dict if note['title'] == button.note_title), None)

        if note_dict is not None:
            self.open_note(note_dict)
            self.original_note_title = button.note_title

    def delete_note(self):
        if self.last_note_title == '':
            QMessageBox.warning(self, 'Error', 'No notes to delete')
            return
        
        confirmation = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this note?', QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.No:
            return

        try:
            with open(self.case_file, 'r') as file:
                try:
                    notes_dict = json.load(file)
                except json.JSONDecodeError:
                    notes_dict = []
        except FileNotFoundError:
            notes_dict = []

        notes = [Note.from_dict(note_dict) for note_dict in notes_dict]

        for i, note in enumerate(notes):
            if note.title == self.last_note_title:
                notes.pop(i)
                break

        notes_dict = [note.to_dict() for note in notes]

        with open(self.case_file, 'w') as file:
            json.dump(notes_dict, file, indent=4)

        self.load_note_buttons()
        self.open_blank_note()

    def get_button_from_title(self, title):
        for widget in self.findChildren(QPushButton):
            if widget is not None and widget.text() == title:
                return widget
        return None
    
    def copy_notes(self):
        if self.case_notes.toPlainText() == '':
            self.main.show_status('No notes to copy', 5000)
            return
        
        text = self.set_notes_content()

        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.main.show_status('Notes copied to clipboard', 5000)

    def get_notes_content(self):
        text = self.case_notes.toPlainText()
        return text

    def copy_options(self):
        options_content = self.get_options_content()

        if options_content:
            clipboard = QApplication.clipboard()
            clipboard.setText(options_content)
            self.main.show_status('Options copied to clipboard', 5000)
            return options_content
        
    def get_options_content(self):
        options_content = ''
        for i in range(0, self.options_layout.rowCount()):
            label_widget = self.options_layout.itemAt(i, QFormLayout.LabelRole).widget()
            value_widget = self.options_layout.itemAt(i, QFormLayout.FieldRole).widget()

            label = label_widget.text()
            value = value_widget.text()

            if value:
                options_content += f'{label}: {value}\n'
        
        return options_content

    def copy_all(self):
        notes = self.get_notes_content()
        options = self.get_options_content()
        
        if notes or options:
            text = f'Case Notes: {notes}\n\n{options}'
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.main.show_status('Notes and options copied to clipboard', 5000)

    def purge_notes(self):
        confirmation = QMessageBox.question(self, 'Confirm Purge', 'Are you sure you want to delete all notes?', QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.No:
            return

        with open(self.case_file, 'w') as file:
            json.dump([], file, indent=4)

        self.load_note_buttons()
        self.open_blank_note()
    
class PlainTextPasteQTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())