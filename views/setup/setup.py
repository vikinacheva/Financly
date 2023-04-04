from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast
from kivy.lang import Builder
from kivy.utils import rgba
from kivy.utils import get_color_from_hex
from data.database import User, Database

Builder.load_file('views/setup/setup.kv')

class Setup(Screen): 
    def submit_starting_budget(self, budget):
        app = App.get_running_app()
        app.budget = float(budget)
    
    def next(self):
        if not self.ids.budget.text:
            return toast("Моля въведете начална сума!")
        if not self.ids.budget.text.isdigit():
            return toast("Сумата не може да съдържа букви!")
        else:
            self.ids.slide.load_next(mode='next')
            self.ids.progress.value = 100
            self.ids.icon.text_color = get_color_from_hex("#f7983c")
            self.ids.icon.icon = "check-circle"

    def next1(self):
        if not self.ids.salary.text:
            return toast("Моля въведете месечен доход (заплата)!")
        if not self.ids.salary.text.isdigit():
            return toast("Сумата не може да съдържа букви!")
        else:
            self.ids.slide.load_next(mode='next')
            self.ids.progress1.value = 100
            self.ids.icon1.text_color = get_color_from_hex("#f7983c")
            self.ids.icon1.icon = "check-circle"
        
    def previous(self):
        self.ids.slide.load_previous()
        self.ids.progress.value = 0
        self.ids.icon.text_color = rgba(34, 56, 97, 255)
        self.ids.icon.icon = "numeric-1-circle"
        
    def previous1(self):
        self.ids.slide.load_previous()
        self.ids.progress1.value = 0
        self.ids.icon1.text_color = rgba(34, 56, 97, 255)
        self.ids.icon1.icon = "numeric-2-circle"
        
    def ready(self):
        if not self.ids.savings.text:
            return toast("Моля въведете желания % за спестяване!")
        try:
            savings = float(self.ids.savings.text)
        except ValueError:
            toast("Процентът трябва да е число!")
            return
        if savings > 100:
            toast("Процентът не може да бъде по-голям от 100!")
            return
        else:
            db = Database()
            user_obj = User()
            user_obj.add_username(App.get_running_app().root.get_screen('register').username.text)
            user_obj.add_email(App.get_running_app().root.get_screen('register').email.text)
            user_obj.add_password(App.get_running_app().root.get_screen('register').password.text)
            user_obj.add_budget(float(self.ids.budget.text))
            user_obj.add_salary(float(self.ids.salary.text))
            user_obj.add_savings(float(self.ids.savings.text))
            db.add_user(user_obj)
            self.manager.current = 'welcome'
    