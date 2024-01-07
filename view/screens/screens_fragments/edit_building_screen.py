import os

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, SlideTransition

from view.screens.main_screen.add_object import AddObject

Builder.load_file(os.getcwd() + "/ui/edit_building_cards_screen.kv")


class EditBuildingCards(Screen):

    data_object = None

    def __init__(self, **kwargs):
        super(EditBuildingCards, self).__init__(**kwargs)

    def on_kv_post(self, add_object):
        self.stylize_object_popup()

    def set_data_object(self, data):
        self.data_object = data
        # print(f"data add object = {data}")
        # "id": id,
        # "address_object": "г. Москва, ул. Автозаводская д. 19, к.1",
        # "date_creation": "30/07/2023",
        # "responsible": "Солоха Николай",
        # "participants": ["Олег Кононов", "Мария Москаленко", "Дмитрий Тарасевич"],
        # "departure_dates": ["30/07/2023", "12/08/2023", "19/08/2023"],
        # "full_name": "Ирина Владимировна Колосова",
        # "email": "895645821@mail.ru",
        # "phone": "8 (999) 452-56-56",
        # "status": "В работе",
        # "contract_num": "ТО-12/01/2023",
        # "img_object": "assets/img/building/building1.jpg"

    def update_size(self, input_data_layout):
        self.ids["img_building_container"].width = input_data_layout.width

    # def fill_data_input_form(self, input_form):
    #     input_form.ids["input_name"].text = self.data_object["address_object"]
    #     input_form.ids["input_type_service"].text = self.data_object["status"]
    #     input_form.ids["input_address"].text = self.data_object["address_object"]
    #     input_form.ids["input_full_name"].text = self.data_object["full_name"]
    #     input_form.ids["input_phone"].text = self.data_object["phone"]
    #     input_form.ids["input_email"].text = self.data_object["email"]

    def stylize_object_popup(self):
        add_object = AddObject(data=self.data_object, callback=None)
        add_object.size_hint = (1, 1)
        add_object.pos_hint = {"right": 1, "top": 1}
        add_object.padding = 0
        add_object.remove_widget(add_object.ids["save_data"])

        form_container = self.ids["edit_object_container"]
        form_container.add_widget(add_object, len(form_container.children))

        input_data_layout = add_object.ids["input_data_layout"]
        input_data_layout.bind(size=lambda *_: self.update_size(input_data_layout))
        # Clock.schedule_once(lambda *_: self.fill_data_input_form(add_object), 1)

    def previous_screen(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "building_cards"
