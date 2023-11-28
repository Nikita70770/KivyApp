from view import MainWindow

import os
import sys
from os.path import dirname

from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivymd.app import MDApp
from kivy.lang.builder import Builder


class MosApplication(MDApp):
    def build(self):
        return Builder.load_file(os.path.join(dirname(__file__), 'interface\main.kv'))


if __name__ == "__main__":
    Window.maximize()
    app = MosApplication()
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    app.run()
