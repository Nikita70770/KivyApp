import kivy
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Ellipse, Line, Canvas, MatrixInstruction
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


# class ScrollZoomImage(Image):
#     def __init__(self, parent):
#         super(ScrollZoomImage, self).__init__()
#         self.matrix = Matrix()
#         self.scale = 1.0
#         self.bind(texture=self._update_texture)
#         self.size_hint=(None, None)
#         self.size = parent.size
#         self.fit_mode="contain"
#
#     def on_touch_up(self, touch):
#         if self.collide_point(*touch.pos):
#             # print("on_touch_up:", touch.profile, touch)
#             if touch.is_mouse_scrolling:
#                 if touch.button == "scrolldown":
#                     print(f"scrolldown\nscatter size = {self.size}\npos = {self.pos}\nscale = {self.scale}\n")
#                     if self.scale > 1.1:
#                         mat = Matrix().scale(0.9, 0.9, 0.9)
#                         self.apply_transform(mat, anchor=touch.pos)
#                         # Clock.schedule_once(self.center_it, 1)
#                 elif touch.button == "scrollup":
#                     print(f"scrollup\nscatter size = {self.size}\npos = {self.pos}\nscale = {self.scale}\n")
#                     if self.scale < 3.0:
#                         mat = Matrix().scale(1.1, 1.1, 1.1)
#                         self.apply_transform(mat, anchor=touch.pos)
#                         # Clock.schedule_once(self.center_it, 1)
#                 # Clock.schedule_once(self.method, 5)
#         return super(ScrollZoomImage, self).on_touch_up(touch)
#
#     def _update_texture(self, *args):
#         self.texture_size = self.texture.size
#
#     def set_building_plan(self, plan_building):
#         self.source = plan_building
#
#     def _update_transform(self):
#         self.matrix = Matrix().scale(self.scale, self.scale, self.scale)
#         self.canvas.before.clear()
#         self.canvas.before.add(MatrixInstruction(matrix=self.matrix))


class ResizableLayout(ScatterLayout):

    def __init__(self, parent):
        super(ResizableLayout, self).__init__()
        self.resizable_plan_building = None
        self.scroll_view = parent
        self.init_layout()

    def init_layout(self):
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.size_hint = (None, None)
        self.size = (self.scroll_view.width * self.scale, self.scroll_view.height * self.scale)
        self.do_translation = False
        self.do_rotation = False
        self.do_scale = True

        self.resizable_plan_building = ResizablePlanBuilding(self)
        self.add_widget(self.resizable_plan_building)

    def set_building_plan(self, plan_building):
        self.resizable_plan_building.set_building_plan(plan_building)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            if touch.is_mouse_scrolling:
                if touch.button == "scrolldown":
                    print(f"scrolldown\nscatter size = {self.size}\npos = {self.pos}\nscale = {self.scale}\n")
                    if self.scale > 1.1:
                        mat = Matrix().scale(0.9, 0.9, 0.9)
                        self.apply_transform(mat, anchor=touch.pos)
                elif touch.button == "scrollup":
                    print(f"scrollup\nscatter size = {self.size}\npos = {self.pos}\nscale = {self.scale}\n")
                    if self.scale < 3.0:
                        mat = Matrix().scale(1.1, 1.1, 1.1)
                        self.apply_transform(mat, anchor=touch.pos)

        return super(ResizableLayout, self).on_touch_up(touch)

    def center_it(self, dt):
        # pass
        mean_x = mean([w.center_x for w in self.children])
        mean_y = mean([w.center_y for w in self.children])
        width = max([w.center_x for w in self.children]) - min([w.center_x for w in self.children])
        height = max([w.center_y for w in self.children]) - min([w.center_y for w in self.children])
        # if width > 0 and height > 0:
        #     optscale = min(self.width / width, self.height / height)
        #     self.scale = max(1.1, min(optscale, 3.0))
        # else:
        #     self.scale = self.scale

        dx, dy = self.to_parent(mean_x, mean_y)
        # self.center = (self.parent.width / 2 + self.center_x - self.scale - dx, self.parent.height / 2 + self.center_y - self.scale - dy)
        self.center = (self.parent.width / 2 + self.center_x - dx, self.parent.height / 2 + self.center_y - dy)
        # print(f"mean_x = {mean_x}\nmean_y = {mean_y}\n(dx, dy) = {(dx, dy)}")
        # print(f"width = {width}\nheight = {height}\n")


class ResizablePlanBuilding(Scatter):
    ZOOM_LEVELS = [0.25, 0.5, 1, 2, 4]

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
        self.size_hint = (None, None)
        # self.size = self.stencil.size
        self.do_rotation = False
        self.do_translation = False
        # self.do_translation = True
        self.do_scale = True

        self.img_plan_building = Image(
            size_hint=(None, None),
            size=(self.stencil.width, self.stencil.height),
            # fit_mode="cover"
            fit_mode="contain"
        )

        # print(f"img_plan_building:\npos={self.img_plan_building.pos},\nsize: {self.img_plan_building.size}\n")
        self.add_widget(self.img_plan_building)
        # self.size = (self.img_plan_building.width, self.img_plan_building.height)
        # Clock.schedule_once(self.method, 3)

        with self.canvas.before:
            Color(0, 0, 1, 1)
            self.rect = Rectangle(
                pos=self.pos,
                size=self.size
            )

    def on_touch_down(self, touch):
        # print(f"on_touch_down: touch.x = {touch.x}, touch.y = {touch.y}")
        with self.img_plan_building.canvas:
            Color(0, 1, 0, 1, mode="rgba"),
            touch.ud["line"] = Line(
                points=(touch.x, touch.y),
                width=3
            )

    def on_touch_move(self, touch):
        # print(f"on_touch_move: touch.x = {touch.x}, touch.y = {touch.y}")
        touch.ud["line"].points += [touch.x, touch.y]

    # def on_touch_up(self, touch):
    #     if self.collide_point(*touch.pos):
    #         # print("on_touch_up:", touch.profile, touch)
    #         if touch.is_mouse_scrolling:
    #             if touch.button == "scrolldown":
    #                 # print(f"scrolldown\nscatter size = {self.size}\npos = {self.pos}\nscale = {self.scale}\n")
    #                 if self.scale > 1.1:
    #                     mat = Matrix().scale(0.9, 0.9, 0.9)
    #                     self.apply_transform(mat, anchor=touch.pos)
    #                     # Clock.schedule_once(self.center_it, 1)
    #             elif touch.button == "scrollup":
    #                 # print(f"scrollup\nscatter size = {self.size}\npos = {self.pos}\nscale = {self.scale}\n")
    #                 if self.scale < 3.0:
    #                     mat = Matrix().scale(1.1, 1.1, 1.1)
    #                     self.apply_transform(mat, anchor=touch.pos)
    #                     # Clock.schedule_once(self.center_it, 1)
    #             # Clock.schedule_once(self.method, 5)
    #     return super(ResizablePlanBuilding, self).on_touch_up(touch)

    # def method(self, *args):
    #     # pass
    #     self.scale = 3.0

    # def center_it(self, dt):
    #     # pass
    #     mean_x = mean([w.center_x for w in self.children])
    #     mean_y = mean([w.center_y for w in self.children])
    #     width = max([w.center_x for w in self.children]) - min([w.center_x for w in self.children])
    #     height = max([w.center_y for w in self.children]) - min([w.center_y for w in self.children])
    #     if width > 0 and height > 0:
    #         optscale = min(self.width / width, self.height / height)
    #         self.scale = max(1.1, min(optscale, 3.0))
    #     else:
    #         self.scale = self.scale
    #
    #     dx, dy = self.to_parent(mean_x, mean_y)
    #     # self.center = (self.parent.width / 2 + self.center_x - self.scale - dx, self.parent.height / 2 + self.center_y - self.scale - dy)
    #     self.center = (self.parent.width / 2 + self.center_x - dx, self.parent.height / 2 + self.center_y - dy)
    #     print(f"mean_x = {mean_x}\nmean_y = {mean_y}\n(dx, dy) = {(dx, dy)}")
    #     print(f"width = {width}\nheight = {height}\n")
