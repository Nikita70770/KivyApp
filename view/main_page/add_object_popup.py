import os

import kivy.metrics
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.graphics import RoundedRectangle, Color
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivymd.uix.boxlayout import MDBoxLayout
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
                "on_release": lambda text=list_items[i]: self.menu_callback(element, text, max_elems)
            } for i in range(len(list_items))
        ]
        MDDropdownMenu(
            caller=caller,
            items=menu_items,
            hor_growth="right",
            position="bottom",
            max_height=dp(200),
            width_mult=4
        ).open()

    def create_element_user(self, element, name):
        rounded_rect = None
        responsible = Button(
            pos_hint={"x": 0, "center_y": 0.5},
            size_hint=(None, None),
            padding=[dp(3), dp(0)],
            halign="center", valign="center",
            text=name,
            font_size=sp(11),
            color=(0, 0, 0, 1),
            background_color=(0, 0, 0, 0)
        )
        with responsible.canvas.before:
            Color(217 / 255, 217 / 255, 217 / 255, 1),
            rounded_rect = RoundedRectangle(
                pos=responsible.pos,
                size=responsible.size,
                radius=[6, ],
            )
        responsible.bind(
            texture_size=responsible.setter('size'),
            pos=lambda *_: self.update_rounded_rect(rounded_rect, responsible),
            size=lambda *_: self.update_rounded_rect(rounded_rect, responsible),
            on_release=lambda *_: self.delete_user(element, responsible)
        )
        return responsible

    def delete_user(self, layout, user):
        count_users = len(layout.children)
        if count_users > 0:
            layout.remove_widget(user)

    def menu_callback(self, element, text, max_count_users):
        if isinstance(element, TextInput):
            element.text = text
        else:
            count_users = len(element.children)
            if not (count_users == max_count_users):
                user_elem = self.create_element_user(element, text)
                element.add_widget(user_elem)

    # def create_element_building(self, container, name_file):
    #     # Контейнер для элементов
    #     container_element = container
    #
    #     #
    #     label_building = Label(
    #         pos_hint={"x": 0, "center_y": 0.5},
    #         size_hint=(None, None),
    #         text=name_file,
    #         font_size=sp(12),
    #         color=(0, 0, 0, 1)
    #     )
    #     label_building.bind(texture_size=label_building.setter("size"))
    #
    #     # img_del_building.bind(texture_size=img_del_building.setter("size"))
    #
    #     btn_del_building = Button(
    #         pos_hint={"x": 0, "center_y": 0.5},
    #         size_hint=(None, None),
    #         # width=img_del_building.size[0],
    #         # height=img_del_building.size[1],
    #         background_color=(0, 1, 0, 0)
    #     )
    #     # btn_del_building.width = img_del_building.size[0]
    #     # btn_del_building.height = img_del_building.size[1]
    #     btn_del_building.bind(
    #         on_release=lambda *_: self.delete_elem_building(container_element)
    #     )
    #
    #     img_del_building = Image(size_hint=(None, None), source="assets/img/remove_elem.png")
    #     # img_del_building.center_x = btn_del_building.center_x
    #     # img_del_building.center_y = btn_del_building.center_y
    #     # img_del_building.bind(texture_size=img_del_building.setter("size"))
    #
    #     btn_del_building.size_hint = (None, None)
    #     # btn_del_building.width = img_del_building.size[0]
    #     # btn_del_building.height = img_del_building.size[1]
    #
    #     btn_del_building.add_widget(img_del_building)
    #
    #     # container_element.add_widget(label_building)
    #     container_element.add_widget(btn_del_building)
    #     with btn_del_building.canvas.before:
    #         Color(71/255, 17/255, 217/255, 1),
    #         rounded_rect = RoundedRectangle(
    #             pos=btn_del_building.pos,
    #             size=btn_del_building.size,
    #             radius=[6, ],
    #         )
    #     return container_element

    def choose_img_building(self, list_ids):
        print(f"list_ids = {list_ids}")
        self.manager.open_file_manager()
        print(f"Данные файла = {self.manager.get_data_file()}")

        name_file = self.manager.get_data_file()

        container_building = self.ids[list_ids[0]]
        labl_file_name = self.ids[list_ids[1]]

        if not name_file is None:
            container_building.opacity = 1
            labl_file_name.text = name_file
        # self.create_element_building(container, name_file)

    def delete_elem_building(self, list_ids):
        container_building = self.ids[list_ids[0]]
        labl_file_name = self.ids[list_ids[1]]

        self.manager.clear_data()
        container_building.opacity = 0
        labl_file_name.text = ""
        print(f"Данные файла = {self.manager.get_data_file()}")

    def save_data_object(self):
        self.close_popup()

    def update_rounded_rect(self, rounded_rect, button):
        rounded_rect.pos = button.pos
        rounded_rect.size = button.size

    # Закрытие всплывающего окна
    def close_popup(self):
        self.dismiss()
