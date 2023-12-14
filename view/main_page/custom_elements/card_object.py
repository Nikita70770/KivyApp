import os.path

from kivy.lang.builder import Builder
from kivymd.uix.card import MDCard

Builder.load_file(os.getcwd() + '/ui/custom_elements/card_object.kv')

class CardObject(MDCard):
    def __init__(self, id):
        super(CardObject, self).__init__(id)
        self.ids["labl_object_id"].text = "#" + str(id)
