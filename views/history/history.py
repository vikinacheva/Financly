from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp, sp
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
    
    def show_transactions(self, incomes, expenses):
        app = App.get_running_app()
        self.monthly_incomes = app.monthly_incomes
        self.monthly_expenses = app.monthly_expenses
        self.monthly_incomes = incomes
        self.monthly_expenses = expenses
        
        self.ids.gl_history.clear_widgets()
        
        total_incomes = 0
        total_expenses = 0
        for income in self.monthly_incomes:
            total_incomes += income[4]
        for expense in self.monthly_expenses:
            total_expenses += expense[4]
          
        for t in expenses:
            tile = ListTile(category_name=str(t[6]))
            tile.tile_id = str(t[0])
            tile.title = str(t[3])
            tile.subtitle = str(t[5])
            tile.amount = str(t[4])
            tile.budget_snapshot = str(t[7])
            tile.expense = True
            tile.icon = category_icons.get(str(t[6]), "icons/default.png")
            tile.icon_color = get_color_from_hex("f8f9fa")
            tile.data = t
            
            self.ids.gl_history.add_widget(tile)

        for t in incomes:
            tile = ListTile(category_name=str(t[6]))
            tile.tile_id = str(t[0])
            tile.title = str(t[3])
            tile.subtitle = str(t[5])
            tile.amount = str(t[4])
            tile.budget_snapshot = str(t[7])
            tile.expense = False
            tile.icon = category_icons.get(str(t[6]), "icons/default.png")
            tile.icon_color = get_color_from_hex("f8f9fa")
            tile.data = t
    
            self.ids.gl_history.add_widget(tile)   
            
        self.ids.monthly_expenses.text = f"-{total_expenses:.2f} лв."
        self.ids.monthly_savings.text = f"{total_incomes - total_expenses:.2f} лв."    