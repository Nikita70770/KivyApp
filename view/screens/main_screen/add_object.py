import os

from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.graphics import RoundedRectangle, Color
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker

from utils.file_manager import FileManager

Builder.load_file(os.getcwd() + "/ui/add_object.kv")


class AddObject(BoxLayout):
    menu_items = {
        "Тип услуги": ["Техническое обследование", "Судебная и досудебная экспертизы",
                       "Независимая экспертиза", "Заключения о соответсвтии", "Обмерные работы"],
        "Ответственный": ["Солоха Николай", "Олег Кононов", "Мария Москаленко", "Дмитрий Тарасевич"],
        "Участники": ["Владимир Соломатин", "Олег Кононов", "Мария Москаленко", "Дамир Ганиев",
                      "Дмитрий Тарасевич", "Ислам Лайпанов"],
        "Статус": ["В работе", "В ожидании", "Завершено"]
    }

    def __init__(self, data, callback):
        super(AddObject, self).__init__()
        Clock.schedule_once(self.init_popup, 0)
        self.callback = callback

        self.fill_data_input_form(data)
        # print(f"data object eeeeeeee = {data}")
        # print(f"data add object = {data}")

    def init_popup(self, dt):
        self.set_style_popup()
        self.manager = FileManager()

    # Функция отвечает за заполнение формы данными
    def fill_data_input_form(self, data):
        if data is not None:
            self.ids["input_name"].text = data["address_object"]
            self.ids["input_type_service"].text = data["status"]
            self.ids["input_address"].text = data["address_object"]
            self.ids["input_full_name"].text = data["full_name"]
            self.ids["input_phone"].text = data["phone"]
            self.ids["input_email"].text = data["email"]

            responsible = self.create_element_user("", data["responsible"])
            self.ids["box_layout_responsible"].add_widget(responsible)

            if not len(data["participants"]) == 0:
                for i in range(len(data["participants"])):
                    count_elems_layout = len(self.ids["box_layout_participant"].children)
                    participant = self.create_element_user("", data["participants"][i])
                    self.ids["box_layout_participant"].add_widget(participant, count_elems_layout)

            self.ids["input_contract_num"].text = data["contract_num"]
            self.ids["inpt_choose_status"].text = data["status"]

            if not len(data["departure_dates"]) == 0:
                for j in range(len(data["departure_dates"])):
                    count_elems_layout = len(self.ids["layout_departure_dates"].children)
                    departure_date = self.create_departure_date(data["departure_dates"][j])
                    self.ids["layout_departure_dates"].add_widget(departure_date)

            file_name = os.path.basename(data["img_object"])
            self.ids["container_building"].opacity = 1
            self.ids["labl_file_name"].text = file_name

    def set_style_popup(self):
        parent = self.ids["grid_layout_popup"].children
        max_width_label = max([child.children[1].texture_size[0] for child in parent])
        for child in parent:
            texture_size = child.children[1].texture_size[0]
            res = (max_width_label - texture_size) + 40
            # child.spacing = kivy.metrics.dp(res * 0.5)
            child.spacing = res

    def show_calendar_dialog(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        departure_date = self.create_departure_date(str(value))
        self.ids["layout_departure_dates"].add_widget(departure_date)

    def create_departure_date(self, date):
        departure_date = date.split("-")
        departure_date.reverse()
        departure_date = "/".join(departure_date)

        date_label = Label(
            pos_hint={ "center_y": 0.5 },
            size_hint=(None, None),
            font_name="assets/fonts/Montserrat-Regular.ttf",
            font_size=sp(10),
            text=departure_date,
            color=(0, 0, 0, 1)
        )
        date_label.bind(texture_size=date_label.setter("size"))
        return date_label

    # Выпадающий список
    def open_dropdown_menu(self, name_field, max_elems, list_id):
        list_items = self.menu_items[name_field]
        # caller = self.ids[id]
        # print(list_id)
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
            font_name="assets/fonts/Montserrat-Regular.ttf",
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
        self.callback()

    def update_rounded_rect(self, rounded_rect, button):
        rounded_rect.pos = button.pos
        rounded_rect.size = button.size
