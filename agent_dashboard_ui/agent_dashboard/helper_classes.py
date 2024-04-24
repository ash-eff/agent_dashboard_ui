class ButtonSelectionMixin:
    def __init__(self):
        self.currently_selected_button = None

    def set_button_selected(self, button):
        if self.currently_selected_button is not None:
            self.currently_selected_button.setStyleSheet("")
        if button is not None:
            self.currently_selected_button = button
            self.currently_selected_button.setStyleSheet("background-color: #90EE90")