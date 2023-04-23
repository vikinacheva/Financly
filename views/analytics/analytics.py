from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from datetime import datetime
from kivy.clock import Clock

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
        
        total_incomes = 0
        total_expenses = 0
        for income in weekly_incomes:
            total_incomes += income[0]
        for expense in weekly_expenses:
            total_expenses += expense[0]
        
        if total_incomes == 0 and total_expenses == 0:
            chart = self.ids.chart
            chart.points = []
            return

        self.ids.incomes_text.text = f"{total_incomes:.2f} лв."
        self.ids.expenses_text.text = f"{total_expenses:.2f} лв."
        
        income_dict = {day: 0 for day in range(7)}
        expense_dict = {day: 0 for day in range(7)}

        for income in weekly_incomes:
            date = datetime.strptime(income[1], '%Y-%m-%d %H:%M:%S').date()
            day = date.weekday()  
            income_dict[day] += income[0]

        for expense in weekly_expenses:
            date = datetime.strptime(expense[1], '%Y-%m-%d %H:%M:%S').date()
            day = date.weekday()  
            expense_dict[day] += expense[0]
        
        points = []
        for day in range(7):
            if income_dict[day] == 0 and expense_dict[day] == 0:
                points.append((0.0001, 0.0001)) 
            elif income_dict[day] == 0:
                points.append((0.0001, expense_dict[day]))
            elif expense_dict[day] == 0:
                points.append((income_dict[day], 0.0001)) 
            else:
                points.append((income_dict[day], expense_dict[day]))
        chart = self.ids.chart  
        chart.points = points