from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.properties import NumericProperty
import sqlite3


Builder.load_file('views/main/main.kv')

class NavBar(CommonElevationBehavior, MDFloatLayout):
    pass
    
class Main(Screen): 
    def on_login(self):
        app = App.get_running_app()
        current_user_id = app.current_user_id
        budget = self.get_budget(current_user_id)
        latest_transactions = self.get_latest_transactions(current_user_id)
        app.budget = budget
        app.latest_transactions = latest_transactions
        self.ids.home.budget = budget
        self.ids.home.show_transactions(latest_transactions)

    def get_budget(self, id):
        self.conn = sqlite3.connect('data/financly.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute('SELECT budget FROM users WHERE users.id = :id', {'id': id})
            result = self.c.fetchone()
            if result is not None:
                return result[0]
            else:
                return None
    
    def get_latest_transactions(self, id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT * FROM (
                SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC LIMIT 10
            )
            UNION ALL
            SELECT * FROM (
                SELECT * FROM incomes WHERE user_id=? ORDER BY date DESC LIMIT 10
            )
            ORDER BY date DESC
            ''',
            (id, id)
        )
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    def if_active (self, instance):
        if instance in self.ids.values():
            current_id = list(self.ids.keys())[list(self.ids.values()).index(instance)]
            for i in range(4):
                if f"nav_icon{i+1}" == current_id:
                    self.ids[f"nav_icon{i+1}"].text_color = get_color_from_hex("#f7983c")
                else:
                    self.ids[f"nav_icon{i+1}"].text_color = get_color_from_hex("#e9f1fa")
