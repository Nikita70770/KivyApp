import os
import sys

from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivymd.app import MDApp
from kivy.lang.builder import Builder


class MosApplication(MDApp):
    def build(self):
        pathFile = os.path.dirname(os.path.abspath(__file__)) + '/ui/main.kv'
        return Builder.load_file(pathFile)


if __name__ == "__main__":
    Window.maximize()
    app = MosApplication()
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    app.run()
