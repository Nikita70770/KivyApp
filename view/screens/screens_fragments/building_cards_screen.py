import os

from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.widget import Widget

from view.screens.main_screen.add_object_popup import AddObjectPopup
from view.screens.main_screen.custom_elements.card_object import CardObject

Builder.load_file(os.getcwd() + "/ui/building_cards_screen.kv")


class BuildingCards(Screen):
    currCount = 0
    countCard = 6
    sizeData = 100
    arrIndex = [0] * 2

    def __init__(self, **kwargs):
        super(BuildingCards, self).__init__(**kwargs)

    def on_kv_post(self, base_widget):
        self.initData()

    def getCountCard(self):
        return len([card for card in self.ids["gridlayout_cards"].children])

    def clear_grid_cards(self):
        self.ids["gridlayout_cards"].clear_widgets()

    def handle_close_popup(self, status_close):
        if status_close:
            self.ids["btn_add_object"].background_color = (0, 0, 0, 0)
            self.ids["img_plus"].source = "assets/img/plus_48.png"

    def initData(self):
        print("Первичная инициализация")
        self.arrIndex[0] = 0
        if self.sizeData == 0:
            self.arrIndex[1] = 0
        elif self.sizeData >= self.countCard:
            self.arrIndex[1] = 6
        else:
            self.arrIndex[1] = self.sizeData
        for i in range(self.arrIndex[1]):
            # print(i)
            self.ids["gridlayout_cards"].add_widget(CardObject((i + 1), self.next_screen))
            # if (i + 1) == self.arrIndex[1]:
            #     print(f"(i + 1) == self.arrIndex[1]")
            #     for j in range(self.arrIndex[1], self.countCard):
            #         print(f"j = {j}")
            #         self.ids["gridlayout_cards"].add_widget(MDLabel(text="Hello"))
        if self.sizeData <= 2:
            for j in range(self.sizeData, 3):
                self.ids["gridlayout_cards"].add_widget(Widget(size_hint=(0.23, 1)))
        print(self.arrIndex)
        print(f"currCount = {self.currCount}")

    def loadNextData(self):
        if self.getCountCard() > 0:
            self.clear_grid_cards()
        diff = self.sizeData - self.arrIndex[1]
        if diff < self.countCard:
            self.arrIndex[0] = self.arrIndex[1]
            self.arrIndex[1] += diff
        else:
            self.arrIndex[0] = self.arrIndex[1]
            self.arrIndex[1] += 6
        for i in range(self.arrIndex[0], self.arrIndex[1]):
            print(i)
            self.ids["gridlayout_cards"].add_widget(CardObject((i + 1), self.next_screen))

        if diff <= 2:
            # print(f"self.arrIndex[1] = {self.arrIndex[1]}")
            for j in range(diff, 3):
                self.ids["gridlayout_cards"].add_widget(Widget(size_hint=(0.23, 1)))
        print(f"diff = {diff}")
        self.ids["scroll_view"].scroll_y = 1
        print("Загрузка карточек после прокрутки")
        print(self.arrIndex)

    def loadPreviousData(self):
        pass

    def btn_add_object_press(self, list_id):
        id_btn_plus = list_id[0]
        id_img_plus = list_id[1]

        self.ids[id_btn_plus].background_color = (0, 0, 0, 1)
        # self.ids[id_img_plus].source = "assets/img/plus_click.png"
        self.ids[id_img_plus].source = "assets/img/plus_click_48.png"

        popup = AddObjectPopup(callback=self.handle_close_popup)
        popup.open()

    def scroll_direction(self, pos_y):
        # print(f"pos_y = {pos_y}")
        if pos_y <= 0:
            self.loadNextData()

    def selected_objects(self, elem, id_cell, text):
        for child in elem.children:
            for subChild in child.children:
                if isinstance(subChild, BoxLayout):
                    subChild.size_hint = (None, None)
                    subChild.size = subChild.parent.size
                    for label in subChild.children:
                        label.color = (98 / 255, 98 / 255, 98 / 255, 1)

        for i, label in enumerate(reversed(self.ids[id_cell].children)):
            if i % 2 == 0:
                label.color = (247 / 255, 2 / 255, 9 / 255, 1)
            else:
                label.color = (0, 0, 0, 1)

        width = self.ids[id_cell].size[0] * 0.985
        height = self.ids[id_cell].size[1] * 0.965

        self.ids[id_cell].size_hint = (None, None)
        self.ids[id_cell].size = (width, height)

        # self.ids["label_name_service"].text = text
        self.update_widget("hide_area_layout", id_cell)

    def update_widget(self, layout, id_cell):
        self.ids[layout].clear_widgets()

        x = self.ids[id_cell].parent.pos[0] + 3
        y = self.ids[id_cell].parent.pos[1] * 0.95

        width = self.ids[id_cell].size[0]
        height = self.ids[id_cell].size[1] / 2.5

        widget = Widget()
        with widget.canvas.before:
            Color(255, 255, 255, 1)
            widget.rect = Rectangle(
                pos=(x, y),
                size=(width, height)
            )
        self.ids["hide_area_layout"].add_widget(widget)

    def next_screen(self, id):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "edit_building_cards"
        # self.manager.get_screen("edit_building_cards").set_data_card(id)
