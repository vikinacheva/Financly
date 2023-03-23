from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.utils import rgba, QueryDict, get_random_color, get_color_from_hex
from kivy.clock import Clock

from widgets.tiles import ListTile

Builder.load_file('views/history/history.kv')

class History(BoxLayout):
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

    def refresh_transactions(self, data):
        grid = self.ids.gl_history
        grid.clear_widgets()

        for t in reversed(data):
            ic = get_color_from_hex("f8f9fa")

            tile = ListTile()
            tile.tile_id = t['id']
            tile.title = t['title']
            tile.subtitle = t['date']
            tile.amount = t['amount']
            tile.extra = t['initial-amount']
            tile.expense = t['expense']
            tile.icon = t['icon']
            tile.icon_color = ic

            grid.add_widget(tile)
