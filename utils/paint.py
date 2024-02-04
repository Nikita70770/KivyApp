import kivy
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line, Canvas
from kivy.graphics.transformation import Matrix
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image, AsyncImage
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter, ScatterPlane
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.widget import Widget
from numpy import mean


class DrawCanvasWidget(StencilView):

    def __init__(self, parent):
        super(DrawCanvasWidget, self).__init__()
        self.draw_widget = None
        self.resizable_picture = None
        self.img_plan_building = None
        self.init_draw_canvas(parent)

    def init_draw_canvas(self, parent):
        self.pos = parent.pos
        self.size = parent.size
        # print(f"StencilView values: \npos = {self.pos}, size = {self.size}")
        with self.canvas.before:
            Color(0, 0, 1, 1, mode="rgba")
            self.rect = Rectangle(
                pos=parent.pos,
                size=parent.size
            )

        # self.img_plan_building = Image(
        #     pos=parent.pos,
        #     size_hint=(None, None),
        #     size=parent.size,
        #     fit_mode="contain"
        # )
        # self.draw_widget = Widget()
        self.resizable_picture = ResizablePlanBuilding(self)

        # self.add_widget(self.img_plan_building)
        # parent.add_widget(self.img_plan_building)
        # self.add_widget(self.draw_widget)
        self.add_widget(self.resizable_picture)

    def set_building_plan(self, plan_building):
        self.resizable_picture.set_building_plan(plan_building)
        # self.img_plan_building.source = plan_building
        # self.img_plan_building.set_building_plan(plan_building)

    def clear_canvas(self): pass
    # self.canvas.clear()
    # self.canvas.clear()
    # print(f"arr = {[ch for ch in self.canvas.children]}")

    # def on_touch_down(self, touch):
    #     # zoom picture
    #     if touch.is_mouse_scrolling:
    #         if touch.button == "scrolldown":
    #             print(f"scrolldown scale = {self.resizable_picture.scale}")
    #             if self.resizable_picture.scale < 10.0:
    #                 self.resizable_picture.scale *= 1.1
    #         elif touch.button == "scrollup":
    #             print(f"scrollup scale = {self.resizable_picture.scale}")
    #             if self.resizable_picture.scale > 0.9:
    #                 self.resizable_picture.scale *= 0.8
    #     else:
    #         with self.canvas:
    #             Color(0, 1, 0, 1, mode="rgba"),
    #             touch.ud["line"] = Line(
    #                 points=(touch.x, touch.y),
    #                 width=3
    #             )

    # def on_touch_down(self, touch):
    #     if not touch.is_mouse_scrolling:
    #         # todo попробовать реализовать рисование в классе Scatter
    #         with self.canvas:
    #             Color(0, 1, 0, 1, mode="rgba"),
    #             touch.ud["line"] = Line(
    #                 points=(touch.x, touch.y),
    #                 width=3
    #             )
    #
    # def on_touch_move(self, touch):
    #     touch.ud["line"].points += [touch.x, touch.y]



class ResizablePlanBuilding(Scatter):

    def __init__(self, parent):
        super(ResizablePlanBuilding, self).__init__()

        self.stencil = parent
        self.img_plan_building = None

        self.init_plan_building()

    def set_building_plan(self, plan_building):
        self.scale = 1.0
        self.img_plan_building.source = plan_building
        self.size = self.img_plan_building.size
        # print(f"Scatter vals:\nheight = {self.height}\nImg vals: height = {self.img_plan_building.height}")

    def init_plan_building(self):
        self.pos = self.stencil.pos
        self.size = self.stencil.size
        self.do_rotation = False
        # self.do_translation = True
        self.do_scale = True

        self.img_plan_building = Image(
            size_hint=(None, None),
            size=self.stencil.size,
            fit_mode="cover"
        )

        with self.canvas.before:
            Color(0, 1, 0, 1)
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size
            )

        print(f"img_plan_building:\npos={self.img_plan_building.pos},\nsize: {self.img_plan_building.size}\n")

        self.add_widget(self.img_plan_building)

    def on_touch_down(self, touch):
        # print(f"on_touch_down: touch.x = {touch.x}, touch.y = {touch.y}")
        with self.canvas:
            Color(1, 0, 0, 1, mode="rgba"),
            touch.ud["line"] = Line(
                points=(touch.x, touch.y),
                width=3
            )

    def on_touch_move(self, touch):
        # print(f"on_touch_move: touch.x = {touch.x}, touch.y = {touch.y}")
        touch.ud["line"].points += [touch.x, touch.y]

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            # print("on_touch_up:", touch.profile, touch)
            if touch.is_mouse_scrolling:
                if touch.button == "scrolldown":
                    print(f"scrolldown scale {self.scale}")
                    if self.scale > 1.1:
                        mat = Matrix().scale(.9, .9, .9)
                        self.apply_transform(mat, anchor=touch.pos)
                elif touch.button == "scrollup":
                    print(f"scrollup scale {self.scale}")
                    if self.scale < 10.0:
                        mat = Matrix().scale(1.1, 1.1, 1.1)
                        self.apply_transform(mat, anchor=touch.pos)

        return super(ResizablePlanBuilding, self).on_touch_up(touch)