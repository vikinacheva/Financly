from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from datetime import datetime
from kivy.utils import rgba, QueryDict, get_random_color, get_color_from_hex
from kivy.properties import NumericProperty, ListProperty
from widgets.tiles import ListTile

Builder.load_file('views/history/history.kv')

category_icons = {
        "Храна": "assets/icons/groceries.png",
        "Дрехи и др.": "assets/icons/shopping.png",
        "Козметика": "assets/icons/cosmetics.png",
        "Транспорт": "assets/icons/transport.png",
        "За дома": "assets/icons/accommodation.png",
        "Здраве": "assets/icons/healthcare.png",
        "Данък": "assets/icons/tax.png",
        "Други": "assets/icons/more-information.png",
        "Заплата": "assets/icons/salary.png",
        "Подарък": "assets/icons/gift-card.png",
        "Инвестиции": "assets/icons/invest.png",
        "Стипендия": "assets/icons/scholarship.png"
    }

class History(Screen):
    monthly_incomes = ListProperty()
    monthly_expenses = ListProperty()
    monthly_savings = NumericProperty()
    
    def show_transactions(self, incomes, expenses):
        app = App.get_running_app()
        self.monthly_savings = app.monthly_savings
        self.monthly_incomes = incomes
        self.monthly_expenses = expenses

        transactions = []
        for income in incomes:
            transactions.append(income)
        for expense in expenses:
            transactions.append(expense)

        transactions.sort(key=lambda t: datetime.strptime(str(t[5]), "%Y-%m-%d %H:%M:%S"), reverse=True)

        self.ids.gl_history.clear_widgets()

        total_incomes = sum(income[4] for income in incomes)
        total_expenses = sum(expense[4] for expense in expenses)

        for t in transactions:
            tile = ListTile(category_name=str(t[6]))
            tile.tile_id = str(t[0])
            tile.title = str(t[3])
            tile.subtitle = str(t[5])
            tile.amount = str(t[4])
            tile.budget_snapshot = str(t[7])
            if t[2]:
                tile.expense = True
            else:
                tile.expense = False
            tile.icon = category_icons.get(str(t[6]), "icons/default.png")
            tile.icon_color = get_color_from_hex("f8f9fa")
            tile.data = t

            self.ids.gl_history.add_widget(tile)

        self.ids.monthly_expenses.text = f"-{total_expenses:.2f} лв."
        self.ids.monthly_savings.text = f"{total_incomes - total_expenses:.2f} / {self.monthly_savings} лв."