import os

import kivy.metrics
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label

from kivy.uix.screenmanager import (
    Screen,
    SlideTransition
)
from kivy.graphics import (
    Line, Color,
    Rectangle, RoundedRectangle
)

from utils.paint import DrawCanvasWidget

Builder.load_file(os.getcwd() + "/ui/building_schematic_ui.kv")


class BuildingSchematic(Screen):
    dropdown_menu_data = [
        "План подвала",
        "План 1-го этажа",
        "План 2-го этажа",
        "План 3-го этажа",
        "План 4-го этажа"
    ]

    plans_data = [
        "assets/img/plans/plan0.png",
        "assets/img/plans/plan1.png",
        "assets/img/plans/plan2.png",
        "assets/img/plans/plan3.png",
        "assets/img/plans/plan4.png"
    ]

    def __init__(self, **kwargs):
        super(BuildingSchematic, self).__init__(**kwargs)

        self.plan_building_layout = None
        self.dropdown_menu = None
        self.draw_canvas = None

        self.init_dropdown_menu()

    def init_draw_canvas(self):
        self.draw_canvas = DrawCanvasWidget(self.plan_building_layout)
        self.plan_building_layout.add_widget(self.draw_canvas)

    def init_dropdown_menu(self):
        self.dropdown_menu = DropDown()
        for i in range(len(self.dropdown_menu_data)):
            title = self.dropdown_menu_data[i]
            item_menu = self.create_item_menu(i, self.dropdown_menu, title)
            # dropdown_menu_layout.add_widget(item_menu)
            self.dropdown_menu.add_widget(item_menu)

    def open_dropdown_menu(self, caller_id):
        caller = self.ids[caller_id]
        self.dropdown_menu.bind(size=lambda *_: self.update_size(self.dropdown_menu))
        self.dropdown_menu.open(caller)

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

    def create_item_menu(self, index, dropdown_menu, item_title):
        item = Button(
            size_hint_y=None,
            text=item_title,
            color=(0, 0, 0, 1),
            background_normal="",
            background_color=(0, 0, 0, 0)
        )
        item.bind(
            texture_size=item.setter("size"),
            on_release=lambda *_: self.item_select_callback(index, dropdown_menu, item_title)
        )
        return item

    def item_select_callback(self, index, dropdown_menu, title):
        self.plan_building_layout = self.ids["plan_building_layout"]
        element = self.plan_building_layout.children[0]

        labl_select_sheet = self.ids["labl_select_sheet"]
        labl_select_sheet.text = title
        labl_select_sheet.color = (215 / 255, 25 / 255, 32 / 255, 1)

        if isinstance(element, Label):
            self.plan_building_layout.remove_widget(element)

        if self.draw_canvas is None:
            self.init_draw_canvas()

        self.draw_canvas.clear_canvas()
        self.draw_canvas.set_building_plan(self.plans_data[index])
        dropdown_menu.dismiss()

    def layers_press(self, list_id):
        layout = self.ids[list_id[0]].parent
        img_layers = self.ids[list_id[1]]

        # btn_layers.parent = (0, 0, 0, 1)
        img_layers.source = "assets/img/layers_white.png"
        with layout.parent.canvas.before:
            Color(0, 0, 0, 1),
            layout.rect = RoundedRectangle(
                pos=layout.pos,
                size=layout.size,
                radius=[kivy.metrics.dp(3), 0, kivy.metrics.dp(3), 0]
            )

    def open_card_screen(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "building_cards"
        self.manager.remove_widget(self)
