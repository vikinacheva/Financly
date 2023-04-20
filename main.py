from kivymd.app import MDApp
import sqlite3
from kivy.uix.screenmanager import ScreenManager
from kivymd.theming import ThemeManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import QueryDict, rgba, get_color_from_hex
from data.database import Database

from views.start import start
from views.login import login
from views.register import register
from views.welcome import welcome
from views.setup import setup
from views.main import main

Window.size = (360, 640)   
    
class Financly(MDApp):    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user_id = None
        self.budget = None
        self.latest_transactions = None
        self.weekly_incomes = 0
        self.weekly_expenses = 0
        
    theme_cls = ThemeManager()
    
    colors = QueryDict()
    fonts = QueryDict()
    fonts.size = QueryDict()
    
    colors.black = get_color_from_hex("#010101")
    colors.white = rgba(255, 255, 255, 255)
    colors.red = get_color_from_hex("d00000")
    colors.green = get_color_from_hex("55a630")
    colors.light = get_color_from_hex("f8f9fa")
    
    colors.primary = rgba(34, 56, 97, 255)
    colors.secondary = get_color_from_hex("#f7983c")
    colors.tertiary = get_color_from_hex("#2c468e")
    
    colors.primary_font = rgba(135, 143, 158, 255)
    colors.secondary_font = rgba(51, 80, 152, 255)
    colors.tertiary_font = rgba(108, 117, 125, 255) 
    colors.input_font = rgba(0, 0, 59, 255)
    
    colors.dash = rgba(178, 178, 178, 255)
    colors.dot = rgba(221, 221, 221, 255)
    colors.icon = get_color_from_hex("#e9f1fa")
    
    fonts.size.h1 = "32sp"
    fonts.size.h2 = "28sp"
    fonts.size.h3 = "24sp"
    fonts.size.h4 = "20sp"
    fonts.size.h5 = "16sp"
    fonts.size.h6 = "12sp"
    
    fonts.heading = 'assets/fonts/Roboto-Bold.ttf'
    fonts.subheading = 'assets/fonts/Roboto-Medium.ttf'
    fonts.body = 'assets/fonts/RobotoCondensed-Regular.ttf'
    fonts.space = 'assets/fonts/RobotoMono-VariableFont_wght.ttf'
    fonts.light = 'assets/fonts/RobotoCondensed-Light.ttf'
    
    def build(self):
        self.db = Database()
        screen_manager = ScreenManager()
        screen_manager.add_widget(login.Login(name = "login"))
        screen_manager.add_widget(main.Main(name = "main"))
        screen_manager.add_widget(register.Register(name = "register"))
        screen_manager.add_widget(setup.Setup(name = "setup"))
        screen_manager.add_widget(start.Start(name = "start"))
        screen_manager.add_widget(welcome.Welcome(name = "welcome"))
        
        return screen_manager   
            
if __name__ == '__main__':
    financly = Financly()
    financly.run()

