import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from view.screens.screens_fragments.building_cards_screen import BuildingCards

Builder.load_file(os.getcwd() + '/ui/main_screen.kv')


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
