from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty
from kivy.utils import rgba, QueryDict, get_random_color
from kivy.clock import Clock
from datetime import datetime, timedelta
from widgets.tiles import ListTile

Builder.load_file('views/analytics/analytics.kv')

class Analytics(Screen):        
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        colors = App.get_running_app().colors

        chart = self.ids.chart
        chart.point_colors = (colors.secondary, colors.secondary_font)
        chart.xlabels = ["Пон", "Вт", "Сря", "Четв", "Пет", "Съб", "Нед"]
        
    def show_transactions(self):
        app = App.get_running_app()
        weekly_incomes = app.weekly_incomes
        weekly_expenses = app.weekly_expenses
        daily_incomes = app.daily_incomes
        daily_expenses = app.daily_expenses
        self.ids.incomes_text.text = f"{weekly_incomes:.2f} лв."
        self.ids.expenses_text.text = f"{weekly_expenses:.2f} лв."
        



    

       