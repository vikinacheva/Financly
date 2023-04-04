from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast
from kivy.lang import Builder
from data.database import User, Database

from kivy.properties import ObjectProperty

Builder.load_file('views/login/login.kv')

class Login(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def show_password(self, checkbox, value):
        if value:
            self.ids.password.password = False
            self.ids.password_text.text = 'Скрий паролата'
        else:
            self.ids.password.password = True
            self.ids.password_text.text = 'Покажи паролата'
            
    def validate(self):
        self.data = Database()
        email = self.ids.email.text
        password = self.ids.password.text
        user = User.from_database(email)
        if not email and not password:
            return toast('Не сте въвели имейл и парола!')
        elif not email:
            return toast('Не сте въвели имейл!')
        elif not password:
            return toast('Не сте въвели парола!')
        val = self.data.select_by_email(email = email)
        if not val:
            toast('Акаунт с този имейл не съществува!')
            self.ids.email.text = ''
            self.ids.password.text = ''
        elif val[2] != password:
            toast('Грешна парола!')
            self.ids.password.text = ''
        else:
            app = App.get_running_app()
            app.current_user_email = email
            starting_budget = app.get_starting_budget()
            self.manager.get_screen('main').user = user
            self.manager.get_screen('main').starting_budget = starting_budget
            self.manager.transition.director = 'left'
            self.manager.current = 'main'
        
