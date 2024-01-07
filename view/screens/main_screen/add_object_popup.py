import os

from kivy.lang.builder import Builder
from kivy.uix.modalview import ModalView

from view.screens.main_screen.add_object import AddObject

Builder.load_file(os.getcwd() + "/ui/add_object_popup.kv")


class AddObjectPopup(ModalView):

    def __init__(self, data, callback):
        super(AddObjectPopup, self).__init__()

        add_obj_fragment = self.ids["add_object_fragment"]
        add_object = AddObject(data, callback=self.close_popup)

        add_obj_fragment.add_widget(add_object, len(add_obj_fragment.children))
        self.handle_close_popup = callback

    def on_dismiss(self):
        self.handle_close_popup(True)

    # Закрытие всплывающего окна
    def close_popup(self):
        self.dismiss()