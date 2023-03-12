from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast
from kivy.lang import Builder
import re
from data.database import User, Database

Builder.load_file('views/register/register.kv')

class Register(Screen):
    def show_password(self, checkbox, value):
        if value:
            self.ids.password_input.password = False
            self.ids.password_text.text = "Скрий паролата"
        else:
            self.ids.password_input.password = True
            self.ids.password_text.text = "Покажи паролата"
        
    def register(self):
        self.u_obj = User()
        self.data = Database()
        username = self.ids.username_input.text
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        confirm_password = self.ids.confirm_password.text
        if not username:
            return toast('Не сте въвели потребителско име!')
        elif ' ' in username:
            return toast('Потребителското име не може да съдържа интервали!')
        elif len(username) < 2 or len(username) > 20:
            return toast('Потребителското име трябва да бъде между 2 и 20 символа!')
        if not email:
            return toast('Не сте въвели имейл!')
        elif '@' not in email:
            return toast('Невалиден имейл адрес!')
        if not password:
            return toast('Не сте въвели парола!')
        elif not re.search(r"\d", password):
            return toast('Паролата трябва да съдържа поне 1 число!')
        elif len(password) < 6 or len(password) > 20:
            return toast('Паролата трябва да бъде между 6 и 20 символа!')
        if not confirm_password:
            return toast('Потвърдете паролата си!')
        if password != confirm_password:
            self.ids.confirm_password.text = ''
            return toast('Паролите не съвпадат!')
        val = self.data.select_by_email(email = email)
        if val is None:
            self.u_obj.add_username(username)
            self.u_obj.add_email(email)
            self.u_obj.add_password(password)
            self.data.add_entry(self.u_obj)
        else:
            toast('Акаунт с този имейл вече съществува!')
            self.ids.username_input.text = ''
            self.ids.username_input.text = ''
            self.ids.username_input.text = ''
        self.manager.current = 'welcome'


