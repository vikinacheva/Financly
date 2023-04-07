from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.clock import Clock
import sqlite3


Builder.load_file('views/main/main.kv')

class NavBar(CommonElevationBehavior, MDFloatLayout):
    pass
    
class Main(Screen):      
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def get_user_data(self, current_user_id):
        app = App.get_running_app()
        current_user_id = app.current_user_id

        conn = sqlite3.connect('data/financly.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (current_user_id,))
        user_data = c.fetchone()
        conn.close()

        return user_data
    
    def if_active (self, instance):
        if instance in self.ids.values():
            current_id = list(self.ids.keys())[list(self.ids.values()).index(instance)]
            for i in range(4):
                if f"nav_icon{i+1}" == current_id:
                    self.ids[f"nav_icon{i+1}"].text_color = get_color_from_hex("#f7983c")
                else:
                    self.ids[f"nav_icon{i+1}"].text_color = get_color_from_hex("#e9f1fa")
