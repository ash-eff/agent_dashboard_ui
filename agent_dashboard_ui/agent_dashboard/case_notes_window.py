import json

from functools import partial

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QFrame
)

class CaseNotesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()
        self.hide()

    def initUI(self): 
        self.main_layout = QVBoxLayout()
        self.outer_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.welcome_label = QLabel("Case Notes", self)
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.welcome_label)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(line)

        self.outer_layout.addLayout(self.left_layout)
        self.outer_layout.addLayout(self.right_layout)
        self.main_layout.addLayout(self.outer_layout)
        self.setLayout(self.main_layout)

    def showEvent(self, event):
        self.clear_layout(self.left_layout) 
        self.clear_layout(self.right_layout)
        self.clear_layout(self.outer_layout)

        self.new_notes_button = QPushButton('New Note', self)
        self.new_notes_button.clicked.connect(self.open_blank_note)
        self.left_layout.addWidget(self.new_notes_button)

        try:
            with open('notes.json', 'r') as file:
                notes = [json.loads(line) for line in file]
        except FileNotFoundError:
            notes = []

        for note in notes:
            button = QPushButton(note['title'])
            button.clicked.connect(partial(self.open_note, note))
            self.left_layout.addWidget(button)

        self.case_title = QLineEdit(self)
        self.case_notes = QTextEdit(self)
        self.save_notes_btn = QPushButton('Save Notes', self)
        self.save_notes_btn.clicked.connect(self.save_notes)

        self.right_layout.addWidget(self.case_title)
        self.right_layout.addWidget(self.case_notes)
        self.right_layout.addWidget(self.save_notes_btn)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
            else:
                self.clear_layout(layout.itemAt(i).layout())

    def open_blank_note(self):
        self.case_title.setText('')
        self.case_notes.setText('')

    def open_note(self, note):
        self.case_title.setText(note['title'])
        self.case_notes.setText(note['notes'])

    def save_notes(self):
        title = ''
        notes = ''
        if self.case_notes.toPlainText() == '' and self.case_title.text() == '':
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
        with open('notes.json', 'a') as file:
            file.write(json.dumps(note) + "\n")

        self.showEvent(None)