import os.path

from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard

Builder.load_file(os.getcwd() + '/ui/custom_elements/card_object.kv')

class CardObject(MDCard):
    def __init__(self, id_card):
        super(CardObject, self).__init__(id_card)
        self.ids["labl_object_id"].text = "#" + str(id_card)

    def card_click(self, id):
        print(f"id card = {id}")
