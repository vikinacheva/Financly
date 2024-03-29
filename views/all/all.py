from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
import sqlite3
from datetime import datetime, timedelta
import calendar


Builder.load_file('views/all/all.kv')

class NavBar(CommonElevationBehavior, MDFloatLayout):
    pass
    
class All(Screen): 
    def on_login(self):
        app = App.get_running_app()
        current_user_id = app.current_user_id
        budget = self.get_budget(current_user_id)
        latest_transactions = self.get_latest_transactions(current_user_id)
        weekly_incomes = self.get_weekly_incomes(current_user_id)
        weekly_expenses = self.get_weekly_expenses(current_user_id)
        monthly_incomes = self.get_monthly_incomes(current_user_id)
        monthly_expenses = self.get_monthly_expenses(current_user_id)
        monthly_savings = self.get_monthly_savings(current_user_id)
        username = self.get_username(current_user_id)
        profile_pic = self.get_profile_picture(current_user_id)
        app.budget = budget
        app.latest_transactions = latest_transactions
        app.weekly_incomes = weekly_incomes
        app.weekly_expenses = weekly_expenses
        app.monthly_incomes = monthly_incomes
        app.monthly_expenses = monthly_expenses
        app.monthly_savings = monthly_savings
        app.username = username
        app.profile_pic = profile_pic
        self.ids.home.budget = budget
        self.ids.home.show_transactions(latest_transactions) 
        self.ids.home.weekly_incomes = weekly_incomes
        self.ids.home.weekly_expenses = weekly_expenses
        self.ids.home.monthly_incomes = monthly_incomes
        self.ids.home.monthly_expenses = monthly_expenses
        self.ids.analytics.show_transactions()
        self.ids.history.show_transactions(monthly_incomes, monthly_expenses)
        self.ids.history.monthly_savings = monthly_savings
        self.ids.account.profile()
        self.ids.account.profile_pic = profile_pic
        
        screen_manager = self.ids.screen_manager
        screen_manager.transition.direction = 'left'
        screen_manager.current = 'screen_home'
        
        self.if_active(self.ids.nav_icon1)
    
    def on_logout(self):
        screen_manager = self.ids.screen_manager
        screen_manager.transition.direction = 'left'
        app = App.get_running_app()
        app.root.current = 'login'
        app.root.transition.direction = 'left'
        app.root.get_screen('login').ids.email.text = ''
        app.root.get_screen('login').ids.password.text = ''

    def get_budget(self, id):
        self.conn = sqlite3.connect('data/financly.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute('SELECT budget FROM users WHERE users.id = :id', {'id': id})
            result = self.c.fetchone()
            if result is not None:
                return result[0]
            else:
                return None
    
    def get_latest_transactions(self, id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        cursor.execute(
            ('''
                SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC LIMIT 10
            '''),
            (id,)
        )
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    def get_weekly_incomes(self, user_id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=7)
        cursor.execute('''SELECT amount, date FROM transactions
                          WHERE user_id = ? AND 
                          is_expense = 0 AND 
                          date >= ? AND date < ?''',
                       (user_id, start_of_week, end_of_week))
        incomes = cursor.fetchall()
        conn.close()
        return incomes
    
    def get_weekly_expenses(self, user_id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        now = datetime.now()
        start_of_week = now - timedelta(days=now.weekday())
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_week = start_of_week + timedelta(days=7)
        cursor.execute('''SELECT amount, date FROM transactions
                          WHERE user_id = ? AND 
                          is_expense = 1 AND 
                          date >= ? AND date < ?''',
                       (user_id, start_of_week, end_of_week))
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_monthly_incomes(self, user_id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()

        now = datetime.now()

        last_day_of_month = calendar.monthrange(now.year, now.month)[1]

        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = datetime(now.year, now.month, last_day_of_month, 23, 59, 59)

        cursor.execute('''SELECT * FROM transactions
                          WHERE user_id = ? AND 
                          date >= ? AND 
                          date <= ? AND 
                          is_expense = 0''',
                       (user_id, start_of_month, end_of_month))
        incomes = cursor.fetchall()
        conn.close()
        return incomes
    
    def get_monthly_expenses(self, user_id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()

        now = datetime.now()

        last_day_of_month = calendar.monthrange(now.year, now.month)[1]

        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = datetime(now.year, now.month, last_day_of_month, 23, 59, 59)

        cursor.execute('''SELECT * FROM transactions
                          WHERE user_id = ? AND 
                          date >= ? AND 
                          date <= ? AND 
                          is_expense = 1''',
                       (user_id, start_of_month, end_of_month))
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_monthly_savings(self, id):
        self.conn = sqlite3.connect('data/financly.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute('SELECT salary, savings FROM users WHERE id = ?', (id,))
            result = self.c.fetchone()
            if result is not None:
                salary, savings = result
                monthly_savings = salary * savings / 100
                return monthly_savings
            else:
                return None
    
    def get_username(self, id):
        self.conn = sqlite3.connect('data/financly.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute('SELECT username FROM users WHERE users.id = :id', {'id': id})
            result = self.c.fetchone()
            if result is not None:
                return result[0]
            else:
                return None
    
    def get_profile_picture(self, id):
        self.conn = sqlite3.connect('data/financly.db')
        self.c = self.conn.cursor()
        with self.conn:
            self.c.execute('SELECT profile_picture FROM users WHERE users.id = :id', {'id': id})
            result = self.c.fetchone()
            if result is not None:
                return result[0]
            else:
                return None

    def if_active (self, instance):
        if instance in self.ids.values():
            current_id = list(self.ids.keys())[list(self.ids.values()).index(instance)]
            for i in range(4):
                if f"nav_icon{i+1}" == current_id:
                    self.ids[f"nav_icon{i+1}"].text_color = get_color_from_hex("#f7983c")
                else:
                    self.ids[f"nav_icon{i+1}"].text_color = get_color_from_hex("#e9f1fa")
