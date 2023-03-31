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
        pass

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
