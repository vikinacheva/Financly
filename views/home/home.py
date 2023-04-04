from kivy.app import App
import time
import os
from datetime import datetime
from random import randint

import sqlite3

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

from kivy.clock import Clock

from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty

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

class Home(BoxLayout):                   
    # def __init__(self, **kw) -> None:
    #     super().__init__(**kw)
    #     Clock.schedule_once(self.render, .1)

    # def render(self, _):
    #     expenses = []
    #     incomes = []
    #     self.refresh_transactions(expenses, incomes)
    
    # def get_expenses(self):
    #     expenses = []
    #     for child in self.ids.gl_transactions.children:
    #         if child.expense:
    #             expenses.append(child.data)
    #     return expenses

    # def get_incomes(self):
    #     incomes = []
    #     for child in self.ids.gl_transactions.children:
    #         if not child.expense:
    #             incomes.append(child.data)
    #     return incomes
    
          
    # def refresh_transactions(self, expenses, incomes):
    #     grid = self.ids.gl_transactions
    #     grid.clear_widgets()
    #     current_budget = self.current_budget

    #     for t in expenses:
    #         ic = get_color_from_hex("f8f9fa")
    #         tile = ListTile()
    #         tile.tile_id = t['id']
    #         tile.title = t['title']
    #         tile.subtitle = t['date']
    #         tile.amount = t['amount']
    #         tile.extra = t['initial-amount']
    #         tile.icon = t['icon']
    #         tile.expense = t['expense']
    #         tile.icon_color = ic
    #         tile.data = t
    #         tile.bind(on_release=self.tile_action)
    #         grid.add_widget(tile)

    #         if t['expense']:
    #             current_budget -= float(t['amount'])

    #     for t in incomes:
    #         ic = get_color_from_hex("f8f9fa")
    #         tile = ListTile()
    #         tile.tile_id = t['id']
    #         tile.title = t['title']
    #         tile.subtitle = t['date']
    #         tile.amount = t['amount']
    #         tile.extra = t['initial-amount']
    #         tile.icon = t['icon']
    #         tile.expense = t['expense']
    #         tile.icon_color = ic
    #         tile.data = t
    #         tile.bind(on_release=self.tile_action)
    #         grid.add_widget(tile)

    #         if not t['expense']:
    #             current_budget += float(t['amount'])

    #     self.current_budget = current_budget
    #     self.ids.current_budget.text = f"{current_budget:.2f} лв."

    # def tile_action(self, inst):
    #     ta = TileAction()
    #     ta.open()

    # def add_new(self, expense=True):
    #     an = AddNew()
    #     an.expense = expense
    #     an.callback = self.add_transaction
    #     an.open()

    # def add_transaction(self, t):
    #     category_name = t['category']
    #     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     icon = category_icons.get(category_name, "icons/default.png")
    #     expense = t['expense']
    #     amount = t['amount']
    #     title = t['title']
    #     budget_id = self.budget_id  

    #     if expense:
    #         sql = "INSERT INTO expenses (budget_id, title, category, date, amount) VALUES (?, ?, ?, ?, ?)"
    #     else:
    #         sql = "INSERT INTO incomes (budget_id, title, category, date, amount) VALUES (?, ?, ?, ?, ?)"
    #     conn = sqlite3.connect('data/financly.db')
    #     cursor = conn.cursor()
    #     cursor.execute(sql, (budget_id, title, category_name, now, amount))
    #     conn.commit()
    #     conn.close()

    #     ic = get_color_from_hex("f8f9fa")
        
    #     now = datetime.now()
    #     dt = datetime.strptime(t['date'], "%Y-%m-%d, %H:%M:%S")
    #     yr = now.year
    #     mnth = now.month
    #     day = now.day

    #     if yr == dt.year and mnth == dt.month:
    #         if day == dt.day:
    #             sub = "Днес"
    #         elif dt.day == day -1:
    #             sub = "Вчера"
    #     else:
    #         sub = t['date']
            
    #     icon = category_icons.get(category_name, "icons/default.png")

    #     tile = ListTile(category_name=category_name)
    #     tile.tile_id = t["cursor.lastrowid"]
    #     tile.title = t["title"]
    #     tile.subtitle = sub
    #     tile.amount = t["amount"]
    #     if expense:
    #         self.current_budget -= float(amount)
    #         tile.extra = f"{float(amount):.2f}"
    #     else:
    #         self.current_budget += float(amount)
    #         tile.extra = f"{float(amount):.2f}"
    #     tile.extra += " лв."
    #     tile.icon = t["icon"]
    #     tile.expense = t["expense"]
    #     tile.icon_color = ic
    #     tile.data = t
    #     tile.bind(on_release=self.tile_action)

    #     self.ids.gl_transactions.add_widget(tile)
    #     self.ids.current_budget.text = f"{self.current_budget:.2f} лв."
    pass

class TileAction(ModalView):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

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
