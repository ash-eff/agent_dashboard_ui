import json
import os

from functools import partial

from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QScrollArea,
    QSizePolicy
)

class CaseNotesWindow(QWidget):
    def __init__(self, dashboard, parent=None):
        super().__init__(parent)
        self.dashboard = dashboard
        self.btn_font_size = self.dashboard.btn_font_size
        self.font_size = self.dashboard.font_size
        self.initUI()
        self.hide()

    def initUI(self): 
        self.main_layout = QVBoxLayout()
        self.outer_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.case_btn_container = QWidget()
        self.case_btn_scroll = QScrollArea()
        self.bottom_button_layout = QHBoxLayout()
        self.last_note_title = ''

        self.case_btn_scroll.setWidgetResizable(True)
        self.case_btn_scroll.setFixedWidth(180)
        self.case_btn_container.setLayout(self.left_layout)
        self.case_btn_scroll.setWidget(self.case_btn_container) 

        self.outer_layout.addWidget(self.case_btn_scroll)
        self.outer_layout.addLayout(self.right_layout)
        self.main_layout.addLayout(self.outer_layout)
        self.main_layout.addLayout(self.bottom_button_layout)
        self.setLayout(self.main_layout)

    def showEvent(self, event):
        self.clear_layout(self.left_layout) 
        self.clear_layout(self.right_layout)
        self.clear_layout(self.bottom_button_layout)

        self.new_note_btn = QPushButton('New Note', self)
        self.new_note_btn.setFont(QFont('Arial', self.btn_font_size))
        self.new_note_btn.setFixedSize(150, 50)
        self.new_note_btn.clicked.connect(self.open_blank_note)
    
        self.save_note_btn = QPushButton('Save Note', self)
        self.save_note_btn.setFont(QFont('Arial', self.btn_font_size))
        self.save_note_btn.setFixedSize(150, 50)
        self.save_note_btn.clicked.connect(self.save_note)

        self.delete_note_btn = QPushButton('Delete Note', self)
        self.delete_note_btn.setFont(QFont('Arial', self.btn_font_size))
        self.delete_note_btn.setStyleSheet('QPushButton {color: black; background-color: red;}')
        self.delete_note_btn.setFixedSize(150, 50)
        self.delete_note_btn.clicked.connect(self.delete_note)

        self.case_title = QLineEdit(self)
        self.case_title.setPlaceholderText('Case Title/Number')
        self.case_title.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.case_title.setMinimumHeight(50) 
        self.case_title.setFont(QFont('Arial', self.font_size))
        self.case_notes = QTextEdit(self)
        self.case_notes.setPlaceholderText('Case Notes')
        self.case_notes.setFont(QFont('Arial', self.font_size))

        self.right_layout.addWidget(self.case_title)
        self.right_layout.addWidget(self.case_notes)
        self.bottom_button_layout.addWidget(self.save_note_btn)
        self.bottom_button_layout.addWidget(self.new_note_btn)
        self.bottom_button_layout.addWidget(self.delete_note_btn)

        self.load_note_buttons()
        self.load_last_note()

    def hideEvent(self, event):
        super().hideEvent(event)
        if self.check_for_valid_note():
            self.save_note()
    
    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
            elif layout.itemAt(i).layout() is not None:
                self.clear_layout(layout.itemAt(i).layout())

    def open_blank_note(self):
        self.case_title.setText('')
        self.case_notes.setText('')
        self.last_note_title = ''

    def open_note(self, note):
        self.case_title.setText(note['title'])
        self.case_notes.setText(note['notes'])
        self.last_note_title = note['title']

    def load_last_note(self):
        try:
            with open('notes.json', 'r') as file:
                try:
                    notes = json.load(file)
                except json.JSONDecodeError:
                    notes = []
        except FileNotFoundError:
            notes = []

        if self.last_note_title != '':
            for note in notes:
                if note['title'] == self.last_note_title:
                    self.open_note(note)
                    break
            else:
                self.open_blank_note()
        else:
            self.open_blank_note()

    def save_note(self):
        title = ''
        notes = ''
        if not self.check_for_valid_note():
            QMessageBox.warning(self, 'Error', 'No notes to save')
            return

        if self.case_title.text() == '':
            title = 'Untitled Case'
        else:
            title = self.case_title.text()

        if self.case_notes.toPlainText() == '':
            notes = 'No notes'
        else:
            notes = self.case_notes.toPlainText()

        note = {'title': title, 'notes': notes}

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
            if existing_note['title'] == title:
                existing_notes[i] = note
                break
        else:
            existing_notes.append(note)
            new_note_added = True

        with open('notes.json', 'w') as file:
            json.dump(existing_notes, file)

        self.last_note_title = title
        if new_note_added:
            self.load_note_buttons()

    def load_note_buttons(self):
        for i in reversed(range(self.left_layout.count())):
            widget = self.left_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        try:
            with open('notes.json', 'r') as file:
                if os.stat('notes.json').st_size != 0:
                    notes = json.load(file)
                else:
                    notes = []
        except FileNotFoundError:
            notes = []

        for note in notes:
            if 'title' in note:
                button = QPushButton(note['title'])
                button.setFixedSize(150, 50)
                button.setFont(QFont('Arial', self.btn_font_size))
                button.clicked.connect(partial(self.open_note, note))
                self.left_layout.addWidget(button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.left_layout.addWidget(spacer)

    def delete_note(self):
        title = self.case_title.text()
        if title == '':
            QMessageBox.warning(self, 'Error', 'No notes to delete')
            return
        
        confirmation = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this note?', QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.No:
            return

        try:
            with open('notes.json', 'r') as file:
                try:
                    notes = json.load(file)
                except json.JSONDecodeError:
                    notes = []
        except FileNotFoundError:
            notes = []

        for i, note in enumerate(notes):
            if note['title'] == title:
                notes.pop(i)
                break

        with open('notes.json', 'w') as file:
            json.dump(notes, file)

        self.load_note_buttons()
        self.open_blank_note()

    def check_for_valid_note(self):
        if self.case_notes.toPlainText() == '' and self.case_title.text() == '':
            return False
        return True