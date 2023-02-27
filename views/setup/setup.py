from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import rgba
from kivy.utils import get_color_from_hex


Builder.load_file('views/setup/setup.kv')

class Setup(Screen):
    
    def next(self):
        self.ids.slide.load_next(mode='next')
        self.ids.progress.value = 100
        self.ids.icon.text_color = get_color_from_hex("#f7983c")
        self.ids.icon.icon = "check-circle"
    
    def next1(self):
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
    

    
    
    