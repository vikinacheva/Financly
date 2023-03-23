import time
import os
from datetime import datetime
from random import randint

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.modalview import ModalView
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict, get_random_color, get_color_from_hex

from kivy.clock import Clock

from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, ListProperty, ColorProperty, NumericProperty

from widgets.tiles import ListTile
from widgets.buttons import FlatButton, IconButton

Builder.load_file('views/home/home.kv')

class Home(BoxLayout):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        trans = [
            {
                'id': 'shopping',
                'title': 'Дрехи',
                'date': 'Днес',
                'amount': '22.00',
                'initial-amount': '12,472',
                'icon': 'assets/icons/shopping.png',
                'expense': True,
            },
            {
                'id': 'groceries',
                'title': 'Храна',
                'date': 'Днес',
                'amount': '54.50',
                'initial-amount': '12,869',
                'icon': 'assets/icons/groceries.png',
                'expense': True,
            },
            {
                'id': 'scholarship',
                'title': 'Стипендия',
                'date': 'Вчера',
                'amount': '40.00',
                'initial-amount': '12,472',
                'icon': 'assets/icons/scholarship.png',
                'expense': False,
            },
            {
                'id': 'cosmetics',
                'title': 'Козметика',
                'date': 'Днес',
                'amount': '720.00',
                'initial-amount': '12,103',
                'icon': 'assets/icons/cosmetics.png',
                'expense': True,
            },
            {
                'id': 'transport',
                'title': 'Транспорт',
                'date': 'Днес',
                'amount': '8.99',
                'initial-amount': '13,757',
                'icon': 'assets/icons/transport.png',
                'expense': True,
            },
            {
                'id': 'salary',
                'title': 'Заплата',
                'date': 'Вчера',
                'amount': '540.00',
                'initial-amount': '12,472',
                'icon': 'assets/icons/salary.png',
                'expense': False,
            },
            {
                'id': 'accommodation',
                'title': 'За дома',
                'date': 'Днес',
                'amount': '540.00',
                'initial-amount': '12,472',
                'icon': 'assets/icons/accommodation.png',
                'expense': True,
            },
        ]
        self.refresh_transactions(trans)

    def refresh_transactions(self, trans):
        grid = self.ids.gl_transactions
        grid.clear_widgets()
        for t in trans:
            ic = get_color_from_hex("f8f9fa")

            tile = ListTile()
            tile.tile_id = t['id']
            tile.title = t['title']
            tile.subtitle = t['date']
            tile.amount = t['amount']
            tile.extra = t['initial-amount']
            tile.icon = t['icon']
            tile.expense = t['expense']
            tile.icon_color = ic
            tile.data = t
            tile.bind(on_release=self.tile_action)

            grid.add_widget(tile)

    def tile_action(self, inst):
        ta = TileAction()
        ta.open()

    def add_new(self, expense=True):
        an = AddNew()
        an.expense = expense
        an.callback = self.add_transaction
        an.open()

    def add_transaction(self, t):
        ic = get_color_from_hex("f8f9fa")

        now = datetime.now()
        dt = datetime.strptime(t['date'], "%Y-%m-%d, %H:%M:%S")
        yr = now.year
        mnth = now.month
        day = now.day

        if yr == dt.year and mnth == dt.month:
            if day == dt.day:
                sub = "Днес"
            elif dt.day == day -1:
                sub = "Вчера"
        else:
            sub = t['date']

        tile = ListTile()
        tile.tile_id = t['id']
        tile.title = t['title']
        tile.subtitle = sub
        tile.amount = t['amount']
        tile.extra = "12,657.09" # Track current balance before add
        # tile.extra = t['initial-amount']
        tile.icon = t['icon']
        tile.expense = t['expense']
        tile.icon_color = ic
        tile.data = t
        tile.bind(on_release=self.tile_action)

        self.ids.gl_transactions.add_widget(tile)

class TileAction(ModalView):
    def __init__(self, **kw) -> None:
        super().__init__(**kw)

class AddNew(ModalView):
    expense = BooleanProperty(False)
    callback = ObjectProperty(print)
    def __init__(self, **kw) -> None:
        super().__init__(**kw)
        Clock.schedule_once(self.render, .1)

    def render(self, _):
        btns = [x for x in range(9, -1, -1)]
        btns.insert(9, ".")
        btns.append("assets/icons/ic_delete.png")

        for b in btns:
            kp = KeyPad()
            kp.source = str(b)
            kp.callback = self.key_press

            try:
                int(b)
            except:
                kp.non_numeric = True

            self.ids.gl_buttons.add_widget(kp)
    
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
            # icon.bind(on_release=self.callback)
        else:
            icon = FlatButton()
            icon.text = value
            icon.font_name = fonts.heading
            icon.font_size = fonts.size.h2
            icon.color = colors.secondary
            # icon.bind(on_release=self.callback)
        
        self.clear_widgets()
        self.add_widget(icon)
    
    def on_callback(self, inst, value):
        self.children[0].bind(on_release=value)
