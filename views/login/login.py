from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast
from kivy.lang import Builder
from data.database import User, Database
from kivy.clock import Clock

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
    
    def message(self):
        return toast("Не можем да Ви помогнем с това!")
        
    def validate(self):
        self.data = Database()
        email = self.ids.email.text
        password = self.ids.password.text
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
        else:
            current_user_id = val[0]
            if val[3] != password:
                toast('Грешна парола!')
                self.ids.password.text = ''
            else:
                app = App.get_running_app()
                app.current_user_id = current_user_id  
                main_screen = self.manager.get_screen('all')
                main_screen.on_login()
                self.manager.transition.director = 'left'
                self.manager.current = 'all'