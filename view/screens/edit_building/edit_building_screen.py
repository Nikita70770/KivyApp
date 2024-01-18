import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, SlideTransition

from view.screens.building_schematic.building_schematic_screen import BuildingSchematic
from view.screens.main_screen.add_object import AddObject

Builder.load_file(os.getcwd() + "/ui/edit_building_cards_ui.kv")


class EditBuildingCards(Screen):

    def __init__(self, data_object):
        super(EditBuildingCards, self).__init__()
        self.stylize_data_input_form(data_object)

    def update_size(self, input_data_layout):
        self.ids["img_building_container"].width = input_data_layout.width

    def stylize_data_input_form(self, data_object):
        add_object = AddObject(data_object, None, self.choose_img_building)
        add_object.size_hint = (1, 1)
        add_object.pos_hint = {"right": 1, "top": 1}
        add_object.padding = 0
        add_object.remove_widget(add_object.ids["save_data"])

        form_container = self.ids["edit_object_container"]
        form_container.add_widget(add_object, len(form_container.children))

        input_data_layout = add_object.ids["input_data_layout"]
        input_data_layout.bind(size=lambda *_: self.update_size(input_data_layout))

    def choose_img_building(self, path_file):
        img_building = self.ids["img_building"]

        if not (img_building is None):
            img_building.source = path_file

    def add_building_plan(self):
        self.open_building_schematic_screen()

    # Переход на страницу с чертежами сооружения
    def open_building_schematic_screen(self):
        building_schematic_screen = BuildingSchematic()
        self.manager.transition = SlideTransition(direction="left")
        self.manager.add_widget(building_schematic_screen)
        self.manager.current = "building_schematic"

    # Переход на страницу с карточками сооружений
    def open_card_screen(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "building_cards"
        self.manager.remove_widget(self)
