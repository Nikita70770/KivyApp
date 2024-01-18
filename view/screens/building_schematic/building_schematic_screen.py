import os

import kivy.metrics
from kivy.graphics import Line, Color, Rectangle
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.uix.boxlayout import MDBoxLayout


Builder.load_file(os.getcwd() + "/ui/building_schematic_ui.kv")


class BuildingSchematic(Screen):
    dropdown_menu_data = [
        "План подвала",
        "План 1-го этажа",
        "План 2-го этажа",
        "План 3-го этажа",
        "План 4-го этажа"
    ]

    def __init__(self, **kwargs):
        super(BuildingSchematic, self).__init__(**kwargs)

    def open_dropdown_menu(self, caller_id):
        caller = self.ids[caller_id]
        labl_select_sheet = self.ids["labl_select_sheet"]
        # dropdown_menu_layout = MDBoxLayout(
        #     orientation="vertical",
        #     size_hint_y=None,
        #     adaptive_height=True,
        #     md_bg_color=(1, 1, 1, 1)
        # )
        dropdown_menu = DropDown()
        for i in range(len(self.dropdown_menu_data)):
            title = self.dropdown_menu_data[i]
            item_menu = self.create_item_menu(dropdown_menu, title)
            # dropdown_menu_layout.add_widget(item_menu)
            dropdown_menu.add_widget(item_menu)

        # dropdown_menu_layout.bind(size=lambda *_: self.update_size(dropdown_menu_layout))
        # dropdown_menu.add_widget(dropdown_menu_layout)
        dropdown_menu.bind(size=lambda *_: self.update_size(dropdown_menu))
        dropdown_menu.open(caller)

    def update_size(self, element):
        with element.canvas.before:
            Color(217 / 255, 217 / 255, 217 / 255, 1, mode="rgba"),
            Line(
                width=2,
                rounded_rectangle=(
                    element.pos[0], element.pos[1],
                    element.size[0], element.size[1],
                    0, 0, kivy.metrics.dp(3), kivy.metrics.dp(3)
                )
            )
            rect_size = 200
            Color(1, 1, 1, 1, mode="rgba"),
            element.rect = Rectangle(
                pos=(element.x + 2.5, element.y + 2.5),
                size=(element.width - 5, element.height - 5)
            )

    def create_item_menu(self, dropdown_menu, item_title):
        item = Button(
            size_hint_y=None,
            text=item_title,
            color=(0, 0, 0, 1),
            background_normal="",
            background_color=(0, 0, 0, 0)
        )
        item.bind(
            texture_size=item.setter("size"),
            on_release=lambda *_: self.item_select_callback(dropdown_menu, item_title)
        )
        return item

    def item_select_callback(self, dropdown_menu, title):
        self.ids["labl_select_sheet"].text = title
        self.ids["labl_select_sheet"].color = (215/255, 25/255, 32/255, 1)
        dropdown_menu.dismiss()

    def open_card_screen(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "building_cards"
        self.manager.remove_widget(self)
