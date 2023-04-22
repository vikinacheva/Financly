from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

Builder.load_file('views/account/account.kv')

class Account(Screen):
    username = StringProperty()
    
    def profile(self):
        app = App.get_running_app()
        self.username = app.username
        self.ids.username.text = f"Здравейте, {self.username}"
        
    def logout(self):
        app = App.get_running_app()
        app.root.transition.direction = 'right'
        app.root.current = "login"
        app.root.get_screen('login').ids.email.text = ""
        app.root.get_screen('login').ids.password.text = ""
        
