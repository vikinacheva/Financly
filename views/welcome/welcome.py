from kivy.uix.screenmanager import Screen
from kivy.utils import rgba
from kivy.lang import Builder

Builder.load_file('views/welcome/welcome.kv')

class Welcome(Screen):
    def current_slide(self, index):
        for i in range(3):
            if index == i:
                self.ids[f'slide{index+1}'].text_color = rgba(35, 56, 99, 255)
            elif index != i:
                self.ids[f'slide{i+1}'].text_color = rgba(221, 221, 221, 255)
               
    def next(self):
        self.ids.carousel.load_next(mode='next')
        if self.ids.slide3.text_color == rgba(35, 56, 99, 255):
            self.manager.current = 'all'
            