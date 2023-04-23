from kivy.lang import Builder
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.screenmanager import Screen
import sqlite3
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty

Builder.load_file('views/account/account.kv')

profile_pics = [
    'assets/profile_pictures/profile1.jpg',
    'assets/profile_pictures/profile2.jpg',
    'assets/profile_pictures/profile3.jpg',
    'assets/profile_pictures/profile4.jpg',
    'assets/profile_pictures/profile5.jpg',
    'assets/profile_pictures/profile6.jpg',
    'assets/profile_pictures/profile7.jpg',
    'assets/profile_pictures/profile8.jpg',
    'assets/profile_pictures/profile9.jpg',
]

class Account(Screen):
    username = StringProperty()
    profile_pic = StringProperty() 

    def profile(self):
        app = App.get_running_app()
        self.username = app.username
        self.profile_pic = app.profile_pic
        self.ids.username.text = f"{self.username}"
        self.ids.profile_picture.source = self.profile_pic
        
    def logout(self):
        app = App.get_running_app()
        app.root.get_screen('main').on_logout()

    def change_profile_picture(self):
        popup = Popup(title="Изберете профилна снимка", size_hint=(0.8, 0.8))
        layout = GridLayout(cols=3, padding=20, spacing=20)

        for pic in profile_pics:
            button = Button(background_normal=pic, background_down=pic, size_hint=(None, None), size=(150, 150))
            button.bind(on_release=lambda button, path=pic: self.set_profile_picture(path))
            layout.add_widget(button)

        popup.content = layout
        popup.open()

    def set_profile_picture(self, path):
        app = App.get_running_app()
        user_id = app.current_user_id
        self.profile_pic = path
        self.ids.profile_picture.source = self.profile_pic

        conn = sqlite3.connect('data/financly.db')
        c = conn.cursor()
        c.execute('UPDATE users SET profile_picture = ? WHERE id = ?', (self.profile_pic, user_id))
        conn.commit()
        conn.close()

        popup = Popup(title="Профилната снимка е сменена", content=Label(text="Профилната снимка е сменена!"), size_hint=(0.8, 0.8))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
