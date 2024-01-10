import os

from kivy.lang.builder import Builder

from kivy.uix.screenmanager import Screen

Builder.load_file(os.getcwd() + "/ui/building_schematic_ui.kv")


class BuildingSchematic(Screen):

    def __init__(self, **kwargs):
        super(BuildingSchematic, self).__init__(**kwargs)
