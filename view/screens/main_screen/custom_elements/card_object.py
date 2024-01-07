import os.path

from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard

Builder.load_file(os.getcwd() + '/ui/custom_elements/card_object.kv')


class CardObject(MDCard):
    def __init__(self, id, callback):
        super(CardObject, self).__init__(id)

        self.init_data(id)
        self.init_card()

        self.callback = callback

    def init_data(self, id):
        self.object_data = {
            "id": id,
            "address_object": "г. Москва, ул. Автозаводская д. 19, к.1",
            "date_creation": "30/07/2023",
            "responsible": "Солоха Николай",
            "participants": ["Олег Кононов", "Мария Москаленко", "Дмитрий Тарасевич"],
            "departure_dates": ["30/07/2023", "12/08/2023", "19/08/2023"],
            "full_name": "Ирина Владимировна Колосова",
            "email": "895645821@mail.ru",
            "phone": "8 (999) 452-56-56",
            "status": "В работе",
            "contract_num": "ТО-12/01/2023",
            "img_object": "assets/img/building/building1.jpg"
        }
    
    def init_card(self):
        self.ids["labl_address"].text = self.object_data["address_object"]
        self.ids["labl_object_id"].text = "#" + str(self.object_data["id"])
        self.ids["labl_val_date_creation"].text = self.object_data["date_creation"]
        self.ids["labl_val_full_name"].text = self.object_data["full_name"]
        self.ids["labl_val_email"].text = self.object_data["email"]
        self.ids["labl_val_phone"].text = self.object_data["phone"]
        self.ids["labl_val_status"].text = self.object_data["status"]
        self.ids["labl_val_contract_number"].text = self.object_data["contract_num"]
        self.ids["img_building"].source = self.object_data["img_object"]
        # self.card_data = {
        #     "id": id,
        #     "name": "г. Москва, ул. Автозаводская д. 19, к.1",
        #     "type_service": "Техническое обследование",
        #     "address_object": "г. Москва, ул. Автозаводская д. 19, к.1",
        #     "full_name": "Ирина Владимировна Колосова",
        #     "phone": "8 (999) 452-56-56",
        #     "email": "895645821@mail.ru",
        #     "responsible": "Солоха Николай",
        #     "participants": ["Олег Кононов", "Мария Москаленко", "Дмитрий Тарасевич"],
        #     "contract_num": "ТО-12/01/2023",
        #     "status": "В работе",
        #     "departure_dates": ["30/07/2023", "12/08/2023", "19/08/2023"],
        #     "img_object": "Screenshot_5.jpg"
        # }

    def card_click(self):
        self.callback(self.object_data)
        # print(f"id card = {self.id_card}")
