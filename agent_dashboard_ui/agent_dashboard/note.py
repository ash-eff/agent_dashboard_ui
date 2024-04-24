import datetime

class Note:
    def __init__(self, notes, title):
        self.notes = notes
        self.title = title if title is not None else "Case Time \n" + datetime.datetime.now().strftime("%H:%M:%S")


    def to_dict(self):
        return {
            'notes': self.notes,
            'title': self.title,
        }

    @classmethod
    def from_dict(cls, note_dict):
        return cls(
            note_dict['notes'],
            note_dict['title']
        )