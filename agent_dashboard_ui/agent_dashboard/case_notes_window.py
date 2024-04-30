import json
import os

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QGroupBox
)

from note import Note

from helper_classes import ButtonSelectionMixin

class CaseNotesWindow(QWidget, ButtonSelectionMixin):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.case_file = main.resource_path('data/notes.json')
        self.main = main
        self.last_note_title = ''
        self.original_note_title = ''
        self.initUI()
        self.hide()

    def initUI(self): 
        # Create all widgets
        self.main_layout = QVBoxLayout()
        self.outer_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_layout = QVBoxLayout()
        self.left_side_group = QGroupBox()
        self.right_side_group = QGroupBox()
        self.scroll_widget = QWidget()
        self.bottom_button_layout = QHBoxLayout()
        self.new_note_btn = QPushButton('New Note', self)      
        self.save_note_btn = QPushButton('Save Note', self)
        self.delete_note_btn = QPushButton('Delete Note', self)
        self.case_notes = PlainTextPasteQTextEdit(self)

        # Set up widget properties
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedWidth(190)
        self.new_note_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.save_note_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.delete_note_btn.setObjectName('warning')
        self.delete_note_btn.setFixedSize(self.main.btn_x_size, self.main.btn_y_size)
        self.case_notes.setPlaceholderText('Case Notes')
        self.left_side_group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        self.outer_layout.setStretch(0,1)
        self.outer_layout.setStretch(1,3)

        # Set up layouts
        self.main_layout.addLayout(self.outer_layout)
        self.main_layout.addLayout(self.bottom_button_layout)
        self.left_side_group.setLayout(self.left_layout)
        self.right_side_group.setLayout(self.right_layout)
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.setLayout(self.main_layout)

        # Add widgets to layouts
        self.right_layout.addWidget(self.case_notes)
        self.left_layout.addWidget(self.scroll_area)
        self.bottom_button_layout.addWidget(self.new_note_btn)
        self.bottom_button_layout.addWidget(self.save_note_btn)
        self.bottom_button_layout.addWidget(self.delete_note_btn)
        self.outer_layout.addWidget(self.left_side_group)
        self.outer_layout.addWidget(self.right_side_group)

        #connect signals
        self.new_note_btn.clicked.connect(self.open_blank_note)
        self.save_note_btn.clicked.connect(self.save_note)
        self.delete_note_btn.clicked.connect(self.delete_note)

    def showEvent(self, event):
        self.clear_layout(self.scroll_layout) 
        self.load_note_buttons()
        self.load_last_note()
        button = self.get_button_from_title(self.last_note_title)
        if button is not None:
            self.set_button_selected(button)

    def hideEvent(self, event):
        super().hideEvent(event)
        if self.last_note_title == '' or self.last_note_title != self.original_note_title:
            self.save_note()
    
    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
            elif layout.itemAt(i).layout() is not None:
                self.clear_layout(layout.itemAt(i).layout())

    def open_blank_note(self):
        self.case_notes.setText('')
        self.last_note_title = ''
        self.original_note_title = ''

    def open_note(self, note_dict):
        note = Note.from_dict(note_dict)

        self.case_notes.setText(note.notes)
        self.last_note_title = note.title
        self.original_note_title = note.title

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
            self.open_blank_note()

    def save_note(self):
        if self.case_notes.toPlainText() == '':
            return

        notes = self.case_notes.toPlainText()
        title = self.last_note_title if self.last_note_title != '' else None

        note = Note(notes, title)
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
        print(f'type: {type(button)}')
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
    
class PlainTextPasteQTextEdit(QTextEdit):
    def insertFromMimeData(self, source):
        self.insertPlainText(source.text())