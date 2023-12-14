import os

import kivy.metrics
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.uix.modalview import ModalView
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu

Builder.load_file(os.getcwd() + '/ui/add_object_popup.kv')


class AddObjectPopup(ModalView):

    def __init__(self, **kwargs):
        super(AddObjectPopup, self).__init__(**kwargs)
        Clock.schedule_once(self.set_style_popup, 0)

    def set_style_popup(self, dt):
        parent = self.ids["grid_layout_popup"].children
        maxWidthLabel = max([child.children[1].texture_size[0] for child in parent])
        for child in parent:
            texture_size = child.children[1].texture_size[0]
            res = (maxWidthLabel - texture_size) + 40
            child.spacing = kivy.metrics.dp(res * 0.5)

    def status_menu_open(self):
        statuses = ["В работе", "В ожидании", "Завершено"]
        menu_items = [
            {
                "height": kivy.metrics.dp(36),
                "text": statuses[i],
                "viewclass": "OneLineListItem",
                "on_release": lambda text=statuses[i]: self.status_menu_callback(text),
            } for i in range(len(statuses))
        ]
        MDDropdownMenu(
            caller=self.ids["inpt_choose_status"],
            items=menu_items,
            width_mult=len(statuses),
        ).open()

    def type_service_menu_open(self):
        type_services = ["Техническое обследование", "Судебная и досудебная экспертизы",
                         "Независимая экспертиза", "Заключения о соответсвтии", "Обмерные работы"]
        menu_items = [
            {
                "height": kivy.metrics.dp(36),
                "text": type_services[i],
                "viewclass": "OneLineListItem",
                "on_release": lambda text=type_services[i]: self.type_service_menu_callback(text),
            } for i in range(len(type_services))
        ]
        MDDropdownMenu(
            caller=self.ids["inpt_choose_type_service"],
            items=menu_items,
            width_mult=len(type_services),
        ).open()

    def type_service_menu_callback(self, text):
        print(f"text = {text}")

    def status_menu_callback(self, text):
        print(f"text = {text}")

    def close_popup(self):
        self.dismiss()
