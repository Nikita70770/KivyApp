import os

from kivy.properties import ListProperty
from plyer import filechooser


class FileManager:
    selection = []

    def __init__(self, **kwargs):
        super(FileManager, self).__init__(**kwargs)
        # self.data_file = ""
        # self.init_file_manager()

    # def init_file_manager(self):
    #     self.data_file = ""
    # self.manager_open = False

    def open_file_manager(self):
        filechooser.open_file(
            on_selection=self.select_path
        )
        # self.manager_open = True

    def select_path(self, path):
        if path:
            self.selection = path
            print(f"selection = {self.selection}")

    def get_path_file(self):
        if len(self.selection) > 0:
            return self.selection[0]

    def get_file_name(self):
        if len(self.selection) > 0:
            return os.path.basename(self.selection[0])

    def clear_data(self):
        if not len(self.selection) == 0:
            self.selection.clear()
