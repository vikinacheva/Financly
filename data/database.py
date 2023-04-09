import sqlite3
import datetime
import threading

class User():
    def __init__(self, username=None, email=None, password=None, budget=None, salary=None, savings=None, incomes=None, expenses=None):
        self.username = username
        self.email = email
        self.password = password
        self.budget = budget
        self.salary = salary
        self.savings = savings
        self.incomes = incomes if incomes is not None else []
        self.expenses = expenses if expenses is not None else []
        
    def add_username(self, username):
        self.username = username
        
    def add_email(self, email):
        self.email = email
    
    def add_password(self, password):
        self.password = password
        
    def add_budget(self, budget):
        self.budget = budget
    
    def add_salary(self, salary):
        self.salary = salary
        
    def add_savings(self, savings):
        self.savings = savings
        
    def add_income(self, budget_id, title, amount, category):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        db = Database()
        db.add_income(budget_id, title, amount, date, category)
        self.incomes.append((title, amount, date, category))

    def add_expense(self, budget_id, title, amount, category):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        db = Database()
        db.add_expense(budget_id, title, amount, date, category)
        self.expenses.append((title, amount, date, category))
    
    @classmethod
    def from_database(cls, id):
        db = Database()
        user_data = db.select_by_id(id)
        if user_data:
            username, email, password = user_data[:3]
            budget = db.get_budget(id)
            salary = db.get_salary(id)
            savings = db.get_savings(id)
            incomes = db.get_incomes(id)
            expenses = db.get_expenses(id)
            user = cls(username, email, password, budget, salary, savings, incomes, expenses)
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
                profile_picture BLOB,
                budget REAL,
                salary REAL,
                savings REAL
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS incomes(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                amount REAL,
                date TEXT,
                category TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                title TEXT,
                amount REAL,
                date TEXT,
                category TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def add_user(self, user_obj):
        with self.conn:
            self.c.execute('INSERT INTO users(username, email, password, budget, salary, savings) VALUES(:username, :email, :password, :budget, :salary, :savings)',
                        {'username': user_obj.username, 'email': user_obj.email, 'password': user_obj.password, 'budget': user_obj.budget, 'salary': user_obj.salary, 'savings': user_obj.savings})
        self.conn.commit()

    def add_income(self, title, amount, date, category):
        self.c.execute("INSERT INTO incomes (title, amount, date, category) VALUES (::title, :amount, :date, :category)", 
                       {'title': title, 'amount': amount, 'date': date, 'category': category})
        self.conn.commit()

    def add_expense(self, title, amount, date, category):
        self.c.execute("INSERT INTO expenses (title, amount, date, category) VALUES (::title, :amount, :date, :category)", 
                       {'title': title, 'amount': amount, 'date': date, 'category': category})
        self.conn.commit()
    
    def get_budget(self, user_id):
        self.c.execute("SELECT budget FROM users WHERE id = ?", (user_id,))
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
            
    def get_incomes(self, id):
        with self.conn:
            self.c.execute('SELECT title, amount, date, category FROM incomes JOIN users ON users.id = incomes.user_id WHERE users.id = :id',
                           {'id': id})
            return self.c.fetchall()
        
    def get_expenses(self, id):
        with self.conn:
            self.c.execute('SELECT title, amount, date, category FROM expenses JOIN users ON users.id = expenses.user_id WHERE users.id = :id',
                           {'id': id})
            return self.c.fetchall()

    def get_user_by_id(self, user_id):
        with self.conn:
            self.c.execute('SELECT * FROM users WHERE id = :user_id', {'user_id': user_id})
            return self.c.fetchone()

    def update_user(self, user):
        conn = sqlite3.connect("data/financly.db")
        c = conn.cursor()
        c.execute("UPDATE users SET username = ?, email = ?, password = ?, budget = ?, salary = ?, savings = ? WHERE id = ?",
                  (user.username, user.email, user.password, user.budget, user.salary, user.savings, user.id))
        conn.commit()
        conn.close()
    
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