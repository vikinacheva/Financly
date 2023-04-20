from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.utils import rgba, get_color_from_hex, QueryDict
from kivy.properties import ColorProperty, ObjectProperty, BooleanProperty, ListProperty, StringProperty, NumericProperty

Builder.load_string('''
<BarChart>:
    BoxLayout:
        size_hint_x: None
        width: dp(6)
        padding: dp(2)
        canvas.before:
            Color:
                rgba: rgba("#f2f2f2") if root.show_xaxis else [0,0,0,0]
            Rectangle:
                pos: [self.pos[0]+(self.size[0]-dp(1)), self.pos[1]+dp(24)]
                size: [dp(1), self.size[1]-dp(24)]
    BoxLayout:
        orientation: 'vertical'
        padding: dp(2)
        BoxLayout:
            id: box
        BoxLayout:
            id: xlabels
            size_hint_y: None
            height: dp(24)
            padding: dp(2)
            canvas.before:
                Color:
                    rgba: rgba("#f2f2f2") if root.show_yaxis else [0,0,0,0]
                Rectangle:
                    pos: [self.pos[0], self.pos[1]+(self.size[1]-dp(1))]
                    size: [self.size[0], dp(1)]

<Bar>:
    padding: dp(3)

<BarPaint>:
    canvas.before:
        Color:
            rgba: self.bcolor
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.width/2]

<AxisLabel>:
    padding: dp(3)
    Label:
        text: root.text
        text_size: self.size
        shorten: True
        shorten_from: 'right'
        font_size: dp(8)
        color: rgba("#c4c4c4")
        halign: 'center'
        valign: 'middle'
''')

class BarChart(BoxLayout):
    points = ListProperty([])
    point_colors = ListProperty([])
    xlabels = ListProperty([])
    show_xaxis = BooleanProperty(True)
    show_yaxis = BooleanProperty(True)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def on_points(self, *args):
        '''
        '''
        self.redraw()

    def redraw(self):
        box = self.ids.box
        box.clear_widgets()

        if len(self.points) == 0:
            return

        if type(self.points[0]) in [list, tuple]:
            x0 = [x[0] for x in self.points]
            x1 = [x[1] for x in self.points]
            alx = x0+x1
            data = alx
        else:
            data = self.points

        ymin = min(data)
        ymax = max(data)

        for i, p in enumerate(self.points):
            if type(self.points[0]) in [list, tuple]:
                value = (p[0]/ymax, p[1]/ymax)
            else:
                value = p/ymax

            point = Bar()
            point.bar_value = value
            point.bcolor = self.point_colors 
            point.text = str(p)

            box.add_widget(point)
    
    def on_point_colors(self, *args):
        self.redraw()

    def on_xlabels(self, *args):
        box = self.ids.xlabels
        box.clear_widgets()

        for l in self.xlabels:
            label = AxisLabel()
            label.text = str(l).title()

            box.add_widget(label)


class BarPaint(BoxLayout):
    bcolor = ColorProperty([0,0,1,.3])
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

class Bar(BoxLayout):
    bcolor = ObjectProperty([1,0,1,.3])
    text = StringProperty("")
    bar_value = ObjectProperty()
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def on_bar_value(self, *args):
        print(self.bar_value)
        if type(self.bar_value) in [int, float]:

            bp = BarPaint()
            bp.size_hint_y = self.bar_value
            bp.bcolor = self.bcolor
            self.add_widget(bp)

        elif type(self.bar_value) in [list, tuple]:

            for v in self.bar_value:
                self.spacing = 2
                bp = BarPaint()
                bp.size_hint_y = v
                bp.bcolor = self.bcolor
                self.add_widget(bp)
            
    def on_bcolor(self, *args):
        if not self.bcolor:
            return

        if len(self.bcolor) == 2:
            for i, c in enumerate(self.children):
                c.bcolor = self.bcolor[i]
        elif type(self.bcolor) == list and len(self.bcolor) == 4:
            for c in self.children:
                c.bcolor = self.bcolor

class AxisLabel(BoxLayout):
    text = StringProperty("")
    def __init__(self, **kw) -> None:
        super().__init__(**kw)