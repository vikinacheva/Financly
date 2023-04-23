import sqlite3
import datetime
import threading
from PIL import Image
import io

class User():
    def __init__(self, username=None, email=None, password=None, profile_picture = None, budget=None, salary=None, savings=None, transactions=None):
        self.username = username
        self.email = email
        self.password = password
        self.profile_picture = profile_picture
        self.budget = budget
        self.salary = salary
        self.savings = savings
        self.transactions = transactions if transactions is not None else []
        
    def add_username(self, username):
        self.username = username
        
    def add_email(self, email):
        self.email = email
    
    def add_password(self, password):
        self.password = password
    
    def add_profile_picture(self, profile_picture):
        self.profile_picture = profile_picture
        
    def add_budget(self, budget):
        self.budget = budget
    
    def add_salary(self, salary):
        self.salary = salary
        
    def add_savings(self, savings):
        self.savings = savings
        
    def add_transaction(self, user_id, is_expense, title, amount, category, budget_snapshot):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        db = Database()
        db.add_transaction(user_id, is_expense, title, amount, date, category, budget_snapshot)
        self.transactions.append((is_expense, title, amount, date, category, budget_snapshot))
    
    @classmethod
    def from_database(cls, id):
        db = Database()
        user_data = db.select_by_id(id)
        if user_data:
            username, email, password = user_data[:3]
            profile_picture = db.get_profile_picture(id)
            budget = db.get_budget(id)
            salary = db.get_salary(id)
            savings = db.get_savings(id)
            transactions = db.get_transactions(id)
            user = cls(username, email, password, profile_picture, budget, salary, savings, transactions)
            return user
        else:
            return None

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data/financly.db')
        self.c = self.conn.cursor()
        self.lock = threading.Lock()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT UNIQUE,
                password TEXT,
                profile_picture TEXT,
                budget REAL,
                salary REAL,
                savings REAL
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                is_expense BOOL,
                title TEXT,
                amount REAL,
                date TEXT,
                category TEXT,
                budget_snapshot TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def add_user(self, user_obj):
        if user_obj.profile_picture is None:
            user_obj.profile_picture = "assets/icons/user.png"
        with self.conn:
            self.c.execute('INSERT INTO users(username, email, password, profile_picture, budget, salary, savings) VALUES(:username, :email, :password, :profile_picture, :budget, :salary, :savings)',
                            {'username': user_obj.username, 'email': user_obj.email, 'password': user_obj.password, 'profile_picture': user_obj.profile_picture, 'budget': user_obj.budget, 'salary': user_obj.salary, 'savings': user_obj.savings})
        self.conn.commit()

    def add_transaction(self, is_expense, title, amount, date, category, budget_snapshot):
        self.c.execute("INSERT INTO transactions (is_expense, title, amount, date, category, budget_snapshot) VALUES (:is_expense, :title, :amount, :date, :category, :budget_snapshot)", 
                       {'is_expense' : is_expense, 'title': title, 'amount': amount, 'date': date, 'category': category, 'budget_snapshot' : budget_snapshot})
        self.conn.commit()
    
    def get_budget(self, user_id):
        self.c.execute("SELECT budget FROM users WHERE id = ?", (user_id,))
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
            
    def get_salary(self, id):
        with self.conn:
            self.c.execute('SELECT salary FROM users WHERE users.id = :id', {'id': id})
            result = self.c.fetchone()
            if result is not None:
                return result[0]
            else:
                return None
            
    def get_savings(self, id):
        with self.conn:
            self.c.execute('SELECT savings FROM users WHERE users.id = :id', {'id': id})
            result = self.c.fetchone()
            if result is not None:
                return result[0]
            else:
                return None
            
    def get_transactions(self, id):
        with self.conn:
            self.c.execute('SELECT is_expense, title, amount, date, category, budget_snapshot FROM transactions JOIN users ON users.id = transactions.user_id WHERE users.id = :id',
                           {'id': id})
            return self.c.fetchall()

    def get_user_by_id(self, user_id):
        with self.conn:
            self.c.execute('SELECT * FROM users WHERE id = :user_id', {'user_id': user_id})
            return self.c.fetchone()
    
    def select_by_id(self, id):
        with self.conn:
            self.c.execute('SELECT * FROM users WHERE id = (:id)',
                           {'id' : id})
            return self.c.fetchone()
    
    def select_by_email(self, email):
        with self.conn:
            self.c.execute('SELECT * FROM users WHERE email = (:email)',
                           {'email' : email})
            return self.c.fetchone()
    
    def __del__(self):
        self.conn.close()