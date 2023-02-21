from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast
from kivy.lang import Builder
from data.database import User, Database

Builder.load_file('views/login/login.kv')

class Login(Screen):
    
    def show_password(self, checkbox, value):
        if value:
            self.ids.password.password = False
            self.ids.password_text.text = "Скрий паролата"
        else:
            self.ids.password.password = True
            self.ids.password_text.text = "Покажи паролата"
            
    def validate(self):
        self.u_obj = User()
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
        real_email, real_pass = [val, ('', '')]
        if real_email != email:
            toast(f'Добре дошли отново, {self.u_obj.username}!')
        elif real_pass != password:
            toast('Грешна парола!')
        self.manager.current = 'home'