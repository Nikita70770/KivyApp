from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


class MainScreen(Screen):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

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

        self.ids["label_name_service"].text = text
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
