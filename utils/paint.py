import kivy
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line, Canvas
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.stencilview import StencilView
from kivy.uix.widget import Widget


class DrawCanvasWidget(StencilView):

    def __init__(self, parent):
        super(DrawCanvasWidget, self).__init__()
        self.img_plan_building = None
        self.init_draw_canvas(parent)

    def init_draw_canvas(self, parent):
        self.pos = parent.pos
        self.size = parent.size
        # print(f"pos = {parent.pos}, size = {parent.size}")

        # with self.canvas.before:
        #     Color(0, 0, 1, 1, mode="rgba")
        #     self.rect = Rectangle(
        #         pos=parent.pos,
        #         size=parent.size
        #     )

        self.img_plan_building = Image(
            pos=parent.pos,
            size_hint=(None, None),
            size=parent.size,
            fit_mode="contain"
        )
        # self.add_widget(self.img_plan_building)
        parent.add_widget(self.img_plan_building)

    def set_building_plan(self, plan_building):
        self.img_plan_building.source = plan_building

    def clear_canvas(self):
        self.canvas.clear()

    def on_touch_down(self, touch):
        with self.canvas:
            Color(0, 1, 0, 1, mode="rgba"),
            touch.ud["line"] = Line(
                points=(touch.x, touch.y),
                width=3
            )

    def on_touch_move(self, touch):
        touch.ud["line"].points += [touch.x, touch.y]





