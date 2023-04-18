from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty
from kivy.utils import rgba, QueryDict, get_random_color
from kivy.clock import Clock

from widgets.tiles import ListTile

Builder.load_file('views/analytics/analytics.kv')

class Analytics(Screen):        
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        points = [(20, 10), (15, 32), (45, 24), (87, 38), (34, 27), (98, 54), (56, 90)]
        colors = App.get_running_app().colors

        chart = self.ids.chart
        chart.point_colors = (colors.secondary, colors.secondary_font)
        chart.points = points
        chart.xlabels = ["Пон", "Вт", "Сря", "Четв", "Пет", "Съб", "Нед"]
        
    def show_weekly_transactions(self):
        app = App.get_running_app()
        self.ids.incomes_text.text = f"{app.weekly_incomes:.2f} лв."
        self.ids.expenses_text.text = f"{app.weekly_expenses:.2f} лв."    



    

       