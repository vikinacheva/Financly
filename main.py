from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from kivy.utils import rgba
from kivy.utils import get_color_from_hex
from views.start import start
from views.login import login
from views.register import register
from views.welcome import welcome
from views.home import home

Window.size = (360, 640)   

class Financly(MDApp):
    theme_cls = ThemeManager()
        
    black_color = get_color_from_hex("#010101")
    white_color = rgba(255, 255, 255, 255)
    
    primary_font_color = rgba(34, 56, 97, 255)
    secondary_font_color = rgba(135, 143, 158, 255)
    tertiary_font_color = rgba(51, 80, 152, 255)
    forth_font_color = rgba(108, 117, 125, 255)
    
    input_font_color = rgba(0, 0, 59, 255)
    dash_color = rgba(178, 178, 178, 255)
    
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(home.Home(name = "home"))
        screen_manager.add_widget(start.Start(name = "start"))
        screen_manager.add_widget(login.Login(name = "login"))
        screen_manager.add_widget(register.Register(name = "register"))
        screen_manager.add_widget(welcome.Welcome(name = "welcome"))
        
        return screen_manager   

if __name__ == '__main__':
    LabelBase.register(name='RobotoB', fn_regular='assets/fonts/Roboto-Bold.ttf')
    LabelBase.register(name='RobotoCR', fn_regular='assets/fonts/RobotoCondensed-Regular.ttf')
    LabelBase.register(name='RobotoMono', fn_regular='assets/fonts/RobotoMono-VariableFont_wght.ttf')
    LabelBase.register(name='RobotoCL', fn_regular='assets/fonts/RobotoCondensed-Light.ttf')
    LabelBase.register(name='RobotoM', fn_regular='assets/fonts/Roboto-Medium.ttf')
    
    financly = Financly()
    financly.run()

