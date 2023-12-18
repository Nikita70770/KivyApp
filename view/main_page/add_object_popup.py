import os

import kivy.metrics
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.graphics import RoundedRectangle, Color
from kivy.lang.builder import Builder
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivymd.uix.menu import MDDropdownMenu
from utils.file_manager import FileManager

Builder.load_file(os.getcwd() + '/ui/add_object_popup.kv')


class AddObjectPopup(ModalView):
    menu_items = {
        "Тип услуги": ["Техническое обследование", "Судебная и досудебная экспертизы",
                       "Независимая экспертиза", "Заключения о соответсвтии", "Обмерные работы"],
        "Ответственный": ["Солоха Николай", "Олег Кононов", "Мария Москаленко", "Дмитрий Тарасевич"],
        "Участники": ["Владимир Соломатин", "Олег Кононов", "Мария Москаленко", "Дамир Ганиев",
                      "Дмитрий Тарасевич", "Ислам Лайпанов"],
        "Статус": ["В работе", "В ожидании", "Завершено"]
    }

    def __init__(self, **kwargs):
        super(AddObjectPopup, self).__init__(**kwargs)
        Clock.schedule_once(self.initPopup, 0)

    def initPopup(self, dt):
        self.set_style_popup()
        self.manager = FileManager()

    def set_style_popup(self):
        parent = self.ids["grid_layout_popup"].children
        max_width_label = max([child.children[1].texture_size[0] for child in parent])
        for child in parent:
            texture_size = child.children[1].texture_size[0]
            res = (max_width_label - texture_size) + 40
            # child.spacing = kivy.metrics.dp(res * 0.5)
            child.spacing = res

    # Выпадающий список
    def open_dropdown_menu(self, name_field, max_elems, list_id):
        list_items = self.menu_items[name_field]
        # caller = self.ids[id]
        print(list_id)
        caller = self.ids[list_id[0]]
        element = self.ids[list_id[1]]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "height": dp(36),
                "text": list_items[i],
                "font_style": "Caption",
                "on_release": lambda text = list_items[i]: self.menu_callback(element, text, max_elems)
            } for i in range(len(list_items))
        ]
        MDDropdownMenu(
            caller = caller,
            items = menu_items,
            hor_growth = "right",
            position = "bottom",
            max_height = dp(200),
            width_mult = 4
        ).open()

    def menu_callback(self, element, text, max_count_users):
        if isinstance(element, TextInput):
            element.text = text
        else:
            count_users = len(element.children)
            if not(count_users == max_count_users):
                user = self.create_user(element, text)
                element.add_widget(user)

    def create_user(self, element, name):
        rounded_rect = None
        responsible = Button(
            pos_hint = { "x": 0, "center_y": 0.5 },
            size_hint = (None, None),
            padding = [dp(3), dp(0)],
            halign = "center", valign = "center",
            text = name,
            font_size = kivy.metrics.sp(11),
            color = (0, 0, 0, 1),
            background_color = (0, 0, 0, 0)
        )
        with responsible.canvas.before:
            Color(217 / 255, 217 / 255, 217 / 255, 1),
            rounded_rect = RoundedRectangle(
                pos = responsible.pos,
                size = responsible.size,
                radius = [6, ],
            )
        responsible.bind(
            texture_size = responsible.setter('size'),
            pos = lambda *_: self.update_rounded_rect(rounded_rect, responsible),
            size = lambda *_: self.update_rounded_rect(rounded_rect, responsible),
            on_release = lambda *_: self.delete_user(element, responsible)
        )
        return responsible

    def delete_user(self, layout, user):
        count_users = len(layout.children)
        if count_users > 0:
            layout.remove_widget(user)

    def choose_img_building(self):
        self.manager.open_file_manager()
        print(f"Data file = {self.manager.get_data_file()}")

    def save_data_object(self):
        self.close_popup()

    def update_rounded_rect(self, rounded_rect, button):
        rounded_rect.pos = button.pos
        rounded_rect.size = button.size

    # Закрытие всплывающего окна
    def close_popup(self):
        self.dismiss()
