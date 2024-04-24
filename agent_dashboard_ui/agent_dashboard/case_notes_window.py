import json
import os

from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
)

from note import Note

class CaseNotesWindow(QWidget):
    def __init__(self, dashboard, parent=None):
        super().__init__(parent)
        self.dashboard = dashboard
        self.btn_font_size = self.dashboard.btn_font_size
        self.font_size = self.dashboard.font_size
        self.last_note_title = ''
        self.original_note_title = ''
        self.initUI()
        self.hide()

    def initUI(self): 
        # Create all widgets
        self.main_layout = QVBoxLayout()
        self.outer_layout = QHBoxLayout()
        self.upper_layout = QVBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.case_btn_container = QWidget()
        self.case_btn_scroll = QScrollArea()
        self.bottom_button_layout = QHBoxLayout()
        self.new_note_btn = QPushButton('New Note', self)      
        self.save_note_btn = QPushButton('Save Note', self)
        self.delete_note_btn = QPushButton('Delete Note', self)
        self.case_notes = QTextEdit(self)

        # Set up widget properties
        self.case_btn_scroll.setWidgetResizable(True)
        self.case_btn_scroll.setFixedWidth(180)
        self.new_note_btn.setFont(QFont('Arial', self.btn_font_size))
        self.new_note_btn.setFixedSize(self.dashboard.btn_x_size, self.dashboard.btn_y_size)
        self.save_note_btn.setFont(QFont('Arial', self.btn_font_size))
        self.save_note_btn.setFixedSize(self.dashboard.btn_x_size, self.dashboard.btn_y_size)
        self.delete_note_btn.setFont(QFont('Arial', self.btn_font_size))
        self.delete_note_btn.setStyleSheet('QPushButton {color: black; background-color: red;}')
        self.delete_note_btn.setFixedSize(self.dashboard.btn_x_size, self.dashboard.btn_y_size)
        self.case_notes.setPlaceholderText('Case Notes')
        self.case_notes.setFont(QFont('Arial', self.font_size))

        # Set up layouts
        self.case_btn_container.setLayout(self.left_layout)
        self.case_btn_scroll.setWidget(self.case_btn_container) 
        self.outer_layout.addWidget(self.case_btn_scroll)
        self.outer_layout.addLayout(self.right_layout)
        self.outer_layout.addLayout(self.upper_layout)
        self.main_layout.addLayout(self.outer_layout)
        self.main_layout.addLayout(self.bottom_button_layout)
        self.setLayout(self.main_layout)

        # Add widgets to layouts
        self.right_layout.addWidget(self.case_notes)
        self.bottom_button_layout.addWidget(self.new_note_btn)
        self.bottom_button_layout.addWidget(self.save_note_btn)
        self.bottom_button_layout.addWidget(self.delete_note_btn)

        #connect signals
        self.new_note_btn.clicked.connect(self.open_blank_note)
        self.save_note_btn.clicked.connect(self.save_note)
        self.delete_note_btn.clicked.connect(self.delete_note)

    def showEvent(self, event):
        self.clear_layout(self.left_layout) 

        self.load_note_buttons()
        self.load_last_note()

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
            with open('notes.json', 'r') as file:
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
            with open('notes.json', 'r') as file:
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
                self.dashboard.show_status('Case updated successfully', 2000)
                break
        else:
            existing_notes.append(note_dict)
            new_note_added = True

        with open('notes.json', 'w') as file:
            json.dump(existing_notes, file, indent=4)

        self.last_note_title = note_dict['title']
        self.original_note_title = note_dict['title']
        if new_note_added:
            self.dashboard.show_status('Case saved successfully', 2000)
            self.load_note_buttons()

    def load_note_buttons(self):
        for i in reversed(range(self.left_layout.count())):
            widget = self.left_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        try:
            with open('notes.json', 'r') as file:
                if os.stat('notes.json').st_size != 0:
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
                button.setFont(QFont('Arial', self.btn_font_size))
                button.note_title = note.title
                button.clicked.connect(self.open_note_from_button)
                self.left_layout.addWidget(button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_layout.addWidget(spacer)

    def open_note_from_button(self):
        button = self.sender()

        with open('notes.json', 'r') as file:
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
            with open('notes.json', 'r') as file:
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

        with open('notes.json', 'w') as file:
            json.dump(notes_dict, file, indent=4)

        self.load_note_buttons()
        self.open_blank_note()