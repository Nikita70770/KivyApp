import os

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, SlideTransition

from view.screens.main_screen.add_object import AddObject

Builder.load_file(os.getcwd() + "/ui/edit_building_cards_screen.kv")


class EditBuildingCards(Screen):

    def __init__(self, data_object):
        super(EditBuildingCards, self).__init__()
        self.name = "edit_building_cards"
        self.stylize_object_popup(data_object)

    def update_size(self, input_data_layout):
        self.ids["img_building_container"].width = input_data_layout.width

    def stylize_object_popup(self, data_object):
        add_object = AddObject(data=data_object, callback=None)
        add_object.size_hint = (1, 1)
        add_object.pos_hint = {"right": 1, "top": 1}
        add_object.padding = 0
        add_object.remove_widget(add_object.ids["save_data"])

        form_container = self.ids["edit_object_container"]
        form_container.add_widget(add_object, len(form_container.children))

        input_data_layout = add_object.ids["input_data_layout"]
        input_data_layout.bind(size=lambda *_: self.update_size(input_data_layout))

    def previous_screen(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "building_cards"
