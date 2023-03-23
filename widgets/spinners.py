from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty, StringProperty, ColorProperty, ListProperty
from kivy.lang import Builder

Builder.load_string("""
<FlatSpinner>:
    text: ""
    values: []
    font_size: sp(16)
    text_color: rgba("#c4c4c4")
    icon_color: rgba("#c4c4c4")
    canvas.before:
        Color:
            rgba: rgba("#DBDBDB")
        Rectangle:
            pos: self.pos
            size: [self.size[0], dp(1.5)]
    Spinner:
        id: spinner
        text: root.text
        values: root.values
        font_size: root.font_size
        text_size: self.size
        valign: "middle"
        color: root.text_color
        background_normal: ""
        background_color: [0,0,0,0]
        option_cls: root.option_cls
    Label:
        text_size: self.size
        size_hint_x: None
        width: self.height
        valign: "middle"
        halign: "right"
        markup: True
        font_size: sp(24)
        color: app.colors.primary

<SoftSpinner>:
    text: ""
    values: []
    font_size: sp(16)
    padding: [dp(4), dp(2)]
    canvas.before:
        Color:
            rgba: app.colors.light
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: root.radius
    Spinner:
        id: spinner
        text: root.text
        font_name: app.fonts.subheading
        values: root.values
        font_size: app.fonts.size.h5
        text_size: self.size
        valign: "middle"
        color: app.colors.primary
        background_normal: ""
        background_color: [0,0,0,0]
        option_cls: root.option_cls
    Label:
        text_size: self.size
        size_hint_x: None
        width: 400
        valign: "middle"
        halign: "right"
        markup: True
        font_size: app.fonts.size.h3
        color: app.colors.primary

<FlatSpinnerOption>:
    padding: [dp(2), dp(2)]
    size_hint_y: None
    height: dp(42)
    canvas.before:
        Color:
            rgba: rgba("#f2f2f2")
        Rectangle:
            pos: self.pos
            size: self.size
    canvas.after:
        Color:
            rgba: rgba("#c4c4c4")
        Rectangle:
            pos: self.pos
            size: [self.size[0], dp(1.5)]
    Label:
        text: root.text
        text_size: self.size
        font_size: app.fonts.size.h6
        shorten: True
        valign: "middle"
        color: [0,0,0,1]

""")

class SoftSpinner(BoxLayout):
    option_cls = ObjectProperty(Button)
    font_name = StringProperty("")
    radius = ListProperty([4])
    bcolor = ColorProperty([1,1,1,1])
    def __init__(self, **kw):
        super().__init__(**kw)
        self.option_cls = FlatSpinnerOption

    def on_font_name(self, inst, value):
        self.ids.spinner.font_name = value

    def get_text(self):
        return self.ids.spinner.text

class FlatSpinner(BoxLayout):
    option_cls = ObjectProperty(Button)
    font_name = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)
        self.option_cls = FlatSpinnerOption

    def on_font_name(self, inst, value):
        self.ids.spinner.font_name = value

    def get_text(self):
        return self.ids.spinner.text

class FlatSpinnerOption(ButtonBehavior, BoxLayout):
    text = StringProperty("")
    def __init__(self, **kw):
        super().__init__(**kw)