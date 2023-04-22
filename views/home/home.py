from kivy.app import App
import time
import os
from datetime import datetime
from random import randint
from data.database import Database
import sqlite3

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp
from kivy.utils import get_color_from_hex, rgba
from kivymd.toast.kivytoast import toast


from kivy.clock import Clock

from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty, ListProperty

from widgets.tiles import ListTile
from widgets.buttons import FlatButton, IconButton

Builder.load_file('views/home/home.kv')

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

class Home(Screen):    
    budget = NumericProperty()
    latest_transactions = ListProperty()
    weekly_incomes = ListProperty()
    weekly_expenses = ListProperty()
    monthly_incomes = ListProperty()
    monthly_expenses = ListProperty()
        
    def add_new(self, expense=True):
        an = AddNew()
        an.expense = expense
        an.callback = self.add_transaction
        an.open()

    def add_transaction(self, t):
        app = App.get_running_app()
        current_user_id = app.current_user_id
        category_name = t['category']
        date = datetime.strptime(t['date'], "%Y-%m-%d, %H:%M:%S")
        icon = category_icons.get(category_name, "icons/default.png")
        ic = get_color_from_hex("f8f9fa")
        expense = t['expense']
        amount = t['amount']
        title = t['title']
        
        if expense:
            if float(amount) < self.budget:
                self.budget -= float(amount)
                self.weekly_expenses.append(float(amount))
                app.weekly_expenses = self.weekly_expenses
                self.monthly_expenses.append(float(amount))
                app.monthly_expenses = self.monthly_expenses
                sql = "INSERT INTO transactions (user_id, is_expense, title, amount, date, category, budget_snapshot) VALUES (?, true, ?, ?, ?, ?, ?)"
            else:
                self.budget -= float(amount)
                self.weekly_expenses.append(float(amount))
                app.weekly_expenses = self.weekly_expenses
                self.monthly_expenses.append(float(amount))
                app.monthly_expenses = self.monthly_expenses
                sql = "INSERT INTO transactions (user_id, is_expense, title, amount, date, category, budget_snapshot) VALUES (?, true, ?, ?, ?, ?, ?)"
                toast("Надхвърли лимита си!")
                self.ids.budget.color = get_color_from_hex("d00000")
        else:
            if float(amount) > self.budget:
                self.budget += float(amount)
                self.weekly_incomes.append(float(amount))
                app.weekly_incomes = self.weekly_incomes
                self.monthly_incomes.append(float(amount))
                app.monthly_incomes = self.monthly_incomes
                sql = "INSERT INTO transactions (user_id, is_expense, title, amount, date, category, budget_snapshot) VALUES (?, false, ?, ?, ?, ?, ?)"
                toast("Отново на плюс!")
                self.ids.budget.color = rgba(255, 255, 255, 255)
            else:
                self.budget += float(amount)
                self.weekly_incomes.append(float(amount))
                app.weekly_incomes = self.weekly_incomes
                self.monthly_incomes.append(float(amount))
                app.monthly_incomes = self.monthly_incomes
                sql = "INSERT INTO transactions (user_id, is_expense, title, amount, date, category, budget_snapshot) VALUES (?, false, ?, ?, ?, ?, ?)"

        budget_snapshot = f"{float(self.budget):.2f}"
        
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        cursor.execute(sql, (current_user_id, title, amount, date, category_name, budget_snapshot))
        conn.commit()
        conn.close()
        
        latest_transactions = app.root.get_screen('main').get_latest_transactions(current_user_id)
        self.show_transactions(latest_transactions) 
        
        app = App.get_running_app()
        current_user_id = app.current_user_id
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET budget = ? WHERE id = ?', (self.budget, current_user_id))
        conn.commit()
        conn.close()

        self.ids.budget.text = f"{self.budget:.2f} лв."
        app.root.get_screen('main').on_login()
    
    def show_transactions(self, transactions):
        self.latest_transactions = transactions
        self.ids.gl_transactions.clear_widgets()
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

            self.ids.gl_transactions.add_widget(tile)
            
class AddNew(ModalView):
    expense = BooleanProperty(False)
    callback = ObjectProperty(print)
    category_button = ObjectProperty(None)
    expense_categories = ["Храна", "Дрехи и др.", "Козметика", "Транспорт", "За дома", "Здраве", "Данък", "Други"]
    income_categories = ["Заплата", "Подарък", "Инвестиции", "Стипендия", "Други"]

    def __init__(self, **kw):
        super().__init__(**kw)
        self.category_button = self.ids.category_button
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        btns = [x for x in range(9, -1, -1)]
        btns.insert(9, ".")
        btns.append("assets/icons/delete.png")
        
        for b in btns:
            kp = KeyPad()
            kp.source = str(b)
            kp.callback = self.key_press

            try:
                int(b)
            except:
                kp.non_numeric = True

            self.ids.gl_buttons.add_widget(kp)

        self.expense_category_dropdown = DropDown()
        for category in self.expense_categories:
            btn = Button(
                text=category,
                size_hint_y=None,
                height=dp(40)
            )
            btn.bind(on_release=self.expense_category_dropdown.select)
            btn.bind(on_release=lambda btn: self.set_category_text(btn.text))
            btn.bind(on_release=lambda btn: self.select_category(btn.text))
            self.expense_category_dropdown.add_widget(btn)

        self.income_category_dropdown = DropDown()
        for category in self.income_categories:
            btn = Button(
                text=category,
                size_hint_y=None,
                height=dp(40)
            )
            btn.bind(on_release=self.income_category_dropdown.select)
            btn.bind(on_release=lambda btn: self.set_category_text(btn.text))
            btn.bind(on_release=lambda btn: self.select_category(btn.text))
            self.income_category_dropdown.add_widget(btn)

    def set_category_text(self, category):
        self.category_button.text = category

    def show_category_dropdown(self, instance):
        if self.expense:
            self.expense_category_dropdown.open(instance)
        else:
            self.income_category_dropdown.open(instance)

    def select_category(self, category):
        if self.expense:
            categories = self.expense_categories
        else:
            categories = self.income_categories
        self.set_category_text(category)
        self.category = category
        self.update_category_dropdown(categories)

    def update_category_dropdown(self, categories):
        if self.expense:
            dropdown = self.expense_category_dropdown
        else:
            dropdown = self.income_category_dropdown

        dropdown.clear_widgets()
        for category in categories:
            btn = Button(
                text=category,
                size_hint_y=None,
                height=dp(40)
            )
            btn.bind(on_release=dropdown.select)
            btn.bind(on_release=lambda btn: self.set_category_text(btn.text))
            btn.bind(on_release=lambda btn: self.select_category(btn.text))
            dropdown.add_widget(btn)

    def confirm(self):
        if self.ids.title.text == '':
            return toast("Моля въведи заглавие на транзакцията!")
        elif self.ids.category_button.text == 'Избери категория':
            return toast("Моля избери категория!")
        elif self.ids.new_amount.text == "0.00":
            return toast("Моля въведи сума на транзакцията!")
        else:
            self.dismiss()
            icons = os.listdir("assets/icons")
            icon = icons[randint(0, len(icons)-1)]

            icon = os.path.join("assets/icons", icon)
            data = {
                'id': str(time.time()),
                'title': self.ids.title.text.strip(),
                'date': datetime.strftime(datetime.now(), "%Y-%m-%d, %H:%M:%S"),
                'amount': self.ids.new_amount.text.strip(),
                'initial-amount': '0.00',
                'icon': icon,
                'expense': self.expense,
                'category': self.category_button.text,
            }
            self.callback(data)
    
    def key_press(self, inst):
        amount = self.ids.new_amount
        if amount.text == '0.00':
            amount.text = ""
        if type(inst) == FlatButton:
            amount.text += inst.text
        else:
            amount.text = amount.text[: -1]
            if amount.text == "":
                amount.text = "0.00"
                
class KeyPad(ButtonBehavior, AnchorLayout):
    source = StringProperty("")
    non_numeric = BooleanProperty(False)
    callback = ObjectProperty(print)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def on_source(self, inst, value):
        colors = App.get_running_app().colors
        fonts = App.get_running_app().fonts

        if value.startswith("assets"):
            self.padding = dp(10)
            icon = IconButton()
            icon.source = value
        else:
            icon = FlatButton()
            icon.text = value
            icon.font_name = fonts.heading
            icon.font_size = fonts.size.h2
            icon.color = colors.secondary
        
        self.clear_widgets()
        self.add_widget(icon)
    
    def on_callback(self, inst, value):
        self.children[0].bind(on_release=value)
