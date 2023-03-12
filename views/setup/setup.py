from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast
from kivy.lang import Builder
from kivy.utils import rgba
from kivy.utils import get_color_from_hex


Builder.load_file('views/setup/setup.kv')

class Setup(Screen): 
    def next(self):
        if not self.ids.initial_amount.text:
            return toast("Моля въведете начална сума!")
        if not self.ids.initial_amount.text.isdigit():
            return toast("Сумата не може да съдържа букви!")
        else:
            self.ids.slide.load_next(mode='next')
            self.ids.progress.value = 100
            self.ids.icon.text_color = get_color_from_hex("#f7983c")
            self.ids.icon.icon = "check-circle"
        
    
    def next1(self):
        if not self.ids.perma_income.text:
            return toast("Моля въведете месечен доход (заплата)!")
        if not self.ids.perma_income.text.isdigit():
            return toast("Сумата не може да съдържа букви!")
        else:
            self.ids.slide.load_next(mode='next')
            self.ids.progress.value = 100
            self.ids.icon.text_color = get_color_from_hex("#f7983c")
            self.ids.icon.icon = "check-circle"
        
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
            self.manager.current = 'main'
        
    

    
    
    