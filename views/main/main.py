from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
import sqlite3
from datetime import datetime, timedelta


Builder.load_file('views/main/main.kv')

class NavBar(CommonElevationBehavior, MDFloatLayout):
    pass
    
class Main(Screen): 
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
        print(str(monthly_savings))
        username = self.get_username(current_user_id)
        app.budget = budget
        app.latest_transactions = latest_transactions
        app.weekly_incomes = weekly_incomes
        app.weekly_expenses = weekly_expenses
        app.monthly_incomes = monthly_incomes
        app.monthly_expenses = monthly_expenses
        app.monthly_savings = monthly_savings
        app.username = username
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
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        cursor.execute('''SELECT amount, date FROM transactions
                          WHERE user_id = ? AND 
                          date >= ? AND 
                          date <= ? AND 
                          is_expense = 0''',
                       (user_id, start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')))
        incomes = cursor.fetchall()
        conn.close()
        return incomes
    
    def get_weekly_expenses(self, user_id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        cursor.execute('''SELECT amount, date FROM transactions
                          WHERE user_id = ? AND 
                          date >= ? AND 
                          date <= ? AND 
                          is_expense = 1''',
                       (user_id, start_of_week.strftime('%Y-%m-%d'), end_of_week.strftime('%Y-%m-%d')))
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    def get_monthly_expenses(self, user_id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        today = datetime.today()
        start_of_month = datetime(today.year, today.month, 1)
        end_of_month = datetime(today.year, today.month, 1) + timedelta(days=32)
        end_of_month = datetime(end_of_month.year, end_of_month.month, 1) - timedelta(days=1)

        cursor.execute('''SELECT * FROM transactions
                          WHERE user_id = ? AND 
                          date >= ? AND 
                          date <= ? AND 
                          is_expense = 1''',
                       (user_id, start_of_month.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d')))
        expenses = cursor.fetchall()
        conn.close()
        return expenses

    def get_monthly_incomes(self, user_id):
        conn = sqlite3.connect('data/financly.db')
        cursor = conn.cursor()
        today = datetime.today()
        start_of_month = datetime(today.year, today.month, 1)
        end_of_month = datetime(today.year, today.month, 1) + timedelta(days=32)
        end_of_month = datetime(end_of_month.year, end_of_month.month, 1) - timedelta(days=1)

        cursor.execute('''SELECT * FROM transactions
                          WHERE user_id = ? AND 
                          date >= ? AND 
                          date <= ? AND 
                          is_expense = 0''',
                       (user_id, start_of_month.strftime('%Y-%m-%d'), end_of_month.strftime('%Y-%m-%d')))
        incomes = cursor.fetchall()
        conn.close()
        return incomes
    
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

    def if_active (self, instance):
        if instance in self.ids.values():
            current_id = list(self.ids.keys())[list(self.ids.values()).index(instance)]
            for i in range(4):
                if f"nav_icon{i+1}" == current_id:
                    self.ids[f"nav_icon{i+1}"].text_color = get_color_from_hex("#f7983c")
                else:
                    self.ids[f"nav_icon{i+1}"].text_color = get_color_from_hex("#e9f1fa")
