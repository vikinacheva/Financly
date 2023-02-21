from kivy.uix.screenmanager import Screen
from kivymd.toast.kivytoast import toast
from kivy.lang import Builder
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
        if username and not email and not password:
            return toast('Не сте въвели потребителско име, парола и имейл!')
        elif not username:
            return toast('Не сте въвели потребителско име!')
        elif not email:
            return toast('Не сте въвели имейл!')
        elif not password:
            return toast('Не сте въвели парола!')
        val = self.data.select_by_email(email = email)
        if val is None:
            self.u_obj.add_username(username)
            self.u_obj.add_email(email)
            self.u_obj.add_password(password)
            self.data.add_entry(self.u_obj)
        else:
            return toast('Акаунт с този имейл вече съществува!')
        self.manager.current = 'welcome'
        
    # Create a submit button with:
    #    - required fields
    #        * if even one field isn't filled in, a text "Задължително поле!" to appear as a function
    #        * if all fields are filled in correctly, create an account
    #    - checking if the email already exists:
    #        * if the email already exists, a text "Акаунт с този имейл вече съществува!" to appear as a function
    #        * if the same email doesn't already exists, create an account
    #    - confirmation of a password:
    #        * if the two passwords are not the same, a text "Несъвпадащи пароли!" to appear as a function
    #        * if the input is correct, create an account
    #    - password validation of length and symbols:
    #        * if the input is not correct, a text "Неправилно въведена парола!" to appear as a function
    #        * if the input is correct, create an account
    #    - when all of the above is fulfilled:
    #        * save the data from all fields (except confirm password) to the database
    #        * redirect to 'welcome.kv' 
