from kivy.uix.button import Button
from kivy.lang import Builder

from kivy.properties import ColorProperty, ListProperty, StringProperty
from kivy.graphics import RoundedRectangle, Color
from kivy.metrics import dp, sp
from kivy.utils import rgba

Builder.load_string("""
<FlatButton>:
    text_size: self.size
    valign: "middle"
    halign: "center"
    text_size: self.size
    markup: True
    valign: 'middle'
    halign: 'center'

<IconButton>:
    canvas.after:
        Color:
            rgba: [1,1,1,1]
        Rectangle:
            pos: self.pos
            size: self.size
            source: self.source
""")
class FlatButton(Button):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.background_color = [0,0,0,0]
        self.background_down = ""
        self.background_normal = ""
        self.background_disabled = ""
        self.markup = True

class IconButton(FlatButton):
    source = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
