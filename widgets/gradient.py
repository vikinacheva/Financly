from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty, BooleanProperty, ColorProperty
from kivy.metrics import dp, sp
from kivy.utils import rgba

class SoftButton(Button):
    bcolor = ListProperty([rgba("#ffffff"), rgba("#FFC837")])
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_color = [0,0,0,0]
        self.background_normal = ""
        self.background_down = ""
        self.color = [1,1,1,1]

        self.texture = Texture.create(size=self.size, colorfmt='rgba')
        with self.canvas:
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, texture=self.texture, radius=[dp(14)])

        self.bind(size=self.update)
        self.bind(pos=self.update)

    def on_bcolor(self, inst, value):
        self.update()

    def update(self, *args):
        p1_color = [int(x*255) for x in self.bcolor[0]]
        p3_color = p1_color
        p4_color = [int(x*255) for x in self.bcolor[1]]
        p2_color = p4_color
        p = p1_color + p2_color + p3_color + p4_color
        buf = bytes(p)
        texture = Texture.create(size=(2,2), colorfmt='rgba')
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.rect.texture = texture
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.rect.radius = [self.height/2]

class SoftBox(ButtonBehavior, BoxLayout):
    bcolor = ListProperty([rgba("#ffffff"), rgba("#FFC837")])
    vertical = BooleanProperty(False)
    radius = ListProperty([1])
    def __init__(self, **kw):
        super().__init__(**kw)

        self.texture = Texture.create(size=self.size, colorfmt='rgba')
        with self.canvas:
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, texture=self.texture, radius=self.radius)

        self.bind(size=self.update)
        self.bind(pos=self.update)

    def on_radius(self, inst, radius):
        self.rect.radius = radius

    def on_bcolor(self, inst, value):
        self.update()

    def on_vertical(self, *args):
        self.update()

    def update(self, *args):
        p1_color = [int(x*255) for x in self.bcolor[0]]
        p4_color = [int(x*255) for x in self.bcolor[1]]

        p2_color = p1_color if self.vertical else p4_color
        p3_color = p4_color if self.vertical else p1_color
        p = p1_color + p2_color + p3_color + p4_color
        buf = bytes(p)
        texture = Texture.create(size=(2,2), colorfmt='rgba')
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        self.rect.texture = texture
        self.rect.size = self.size
        self.rect.pos = self.pos
