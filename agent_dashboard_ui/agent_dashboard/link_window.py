import json

from PyQt5.QtWidgets import (
    QDialog,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QMessageBox
)

class LinkWindow(QDialog):
    def __init__(self, mode, link_name, parent=None):
        super(LinkWindow, self).__init__(parent)
        self.dashboard = self.parent()
        self.links_file = 'data/links.json'
        self.working_link_name = link_name
        self.mode = mode
        self.link_name_label = QLabel('Link Name:')
        self.link_url_label = QLabel('Link URL:')
        self.link_name = QLineEdit()
        self.link_url = QLineEdit()
        self.add_btn = QPushButton('Add Link')
        self.delete_btn = QPushButton('Delete Link')
        self.update_btn = QPushButton('Update Link')
        layout = QVBoxLayout()
        layout.addWidget(self.link_name_label)
        layout.addWidget(self.link_name)
        layout.addWidget(self.link_url_label)
        layout.addWidget(self.link_url)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.update_btn)
        self.setMinimumSize(400, 100)
        self.setLayout(layout)

        self.add_btn.clicked.connect(self.add_link)
        self.delete_btn.clicked.connect(self.delete_link)
        self.update_btn.clicked.connect(self.update_link)

        if self.mode == 'add':
            self.setup_add_window()
        elif self.mode == 'edit':
            self.setup_edit_window()
        elif self.mode == 'delete':
            self.setup_delete_window()

    def setup_add_window(self):
        self.setWindowTitle('Add Link')
        self.update_btn.hide()
        self.delete_btn.hide()

    def setup_edit_window(self):
        self.setWindowTitle('Edit Link')
        link = self.get_link()
        self.link_name.setText(link['link_name'])
        self.link_url.setText(link['link_url'])
        self.add_btn.hide()
        self.delete_btn.hide()

    def setup_delete_window(self):
        self.setWindowTitle('Delete Link')
        link = self.get_link()
        self.link_name.setText(link['link_name'])
        self.link_url.setText(link['link_url'])
        self.link_name.setReadOnly(True)
        self.link_url.setReadOnly(True)
        self.add_btn.hide()
        self.update_btn.hide()

    def get_link(self):
        with open(self.links_file, 'r') as file:
            links = json.load(file)
            for link in links:
                if link['link_name'] == self.working_link_name:
                    return link

    def add_link(self):
        link_name = self.link_name.text()
        link_url = self.link_url.text()
        if link_name and link_url:
            new_link = {
                'link_name': link_name,
                'link_url': link_url
            }

            if not self.verify_unique(link_name):
                QMessageBox.warning(self, 'Error', 'A link with this name already exists.')   
                return
            
            with open(self.links_file, 'r') as file:
                try:
                    link = json.load(file)
                except json.JSONDecodeError:
                    link = []

            link.append(new_link)

            with open(self.links_file, 'w') as file:
                json.dump(link, file, indent=4)

        self.dashboard.load_links()
        self.close()

    def delete_link(self):
        link = self.get_link()
        with open(self.links_file, 'r') as file:
            links = json.load(file)
            links.remove(link)

        confirmation = QMessageBox.question(self, 'Confirm Deletion', 'Are you sure you want to delete this link?', QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.No:
            return

        with open(self.links_file, 'w') as file:
            json.dump(links, file, indent=4)

        self.dashboard.load_links()
        self.close()

    def update_link(self):
        link = self.get_link()
        link['link_name'] = self.link_name.text()
        link['link_url'] = self.link_url.text()

        with open(self.links_file, 'r') as file:
            links = json.load(file)
            for i, l in enumerate(links):
                if l['link_name'] == self.working_link_name:
                    links[i] = link
        
        if not self.verify_unique(link['link_name']):
            QMessageBox.warning(self, 'Error', 'A link with this name already exists.')   
            return

        with open(self.links_file, 'w') as file:
            json.dump(links, file, indent=4)

        self.dashboard.load_links()
        self.close()

    def verify_unique(self, link_name):
        with open(self.links_file, 'r') as file:
            links = json.load(file)
            for link in links:
                if link['link_name'] == link_name:
                    return False
        return True