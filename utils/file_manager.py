import os

from kivymd.uix.filemanager import MDFileManager
from plyer import filechooser


class FileManager:

    def __init__(self, **kwargs):
        super(FileManager, self).__init__(**kwargs)

    def open_file_manager(self):
        filechooser.open_file(
            on_selection = self.select_path
        )

    def select_path(self, path):
        # self.set_data_file(os.path.basename(path), path)
        # self.data_file = {
        #     "name_file": os.path.basename(path),
        #     "path_to_file": path
        # }
        self.data_file = path

    def get_data_file(self):
        return self.data_file