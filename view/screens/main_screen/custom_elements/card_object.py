import os.path

from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard

Builder.load_file(os.getcwd() + '/ui/custom_elements/card_object.kv')


class CardObject(MDCard):
    def __init__(self, id, callback):
        super(CardObject, self).__init__(id)
        self.id_card = id
        self.callback = callback
        self.ids["labl_object_id"].text = "#" + str(id)

    def card_click(self):
        self.callback(self.id_card)
        print(f"id card = {self.id_card}")
