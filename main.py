from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from views.start import start
from views.login import login
from views.register import register
from views.welcome import welcome
from views.home import home

Window.size = (360, 640)   

class Financly(MDApp):
    theme_cls = ThemeManager()
        
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(register.Register(name = "register"))
        screen_manager.add_widget(home.Home(name = "home"))
        screen_manager.add_widget(start.Start(name = "start"))
        screen_manager.add_widget(login.Login(name = "login"))
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

