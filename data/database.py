import sqlite3
import datetime
import threading

class User():
    def __init__(self, username=None, email=None, password=None, starting_budget=None, savings=None, incomes=None, expenses=None):
        self.username = username
        self.email = email
        self.password = password
        self.starting_budget = starting_budget
        self.savings = savings
        self.incomes = incomes if incomes is not None else []
        self.expenses = expenses if expenses is not None else []
        
        if starting_budget is None and email is not None:
            self.set_starting_budget()
    def set_starting_budget(self):
        db = Database()
        self.starting_budget = db.get_starting_budget(self.email)
    
    def add_username(self, username):
        self.username = username
        
    def add_email(self, email):
        self.email = email
    
    def add_password(self, password):
        self.password = password
        
    def add_starting_budget(self, starting_budget):
        self.starting_budget = starting_budget
        
    def add_savings(self, savings):
        self.savings = savings
        
    def add_income(self, db, budget_id, title, amount, category):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        db.add_income(budget_id, title, amount, date, category)
        self.incomes.append((title, amount, date, category))

    def add_expense(self, db, budget_id, title, amount, category):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        db.add_expense(budget_id, title, amount, date, category)
        self.expenses.append((title, amount, date, category))
    
    @classmethod
    def from_database(cls, email):
        db = Database()
        user_data = db.select_by_email(email)
        if user_data:
            username, email, password = user_data[:3]
            starting_budget = db.get_starting_budget(email)
            savings = db.get_savings(email)
            incomes = db.get_incomes(email)
            expenses = db.get_expenses(email)
            user = cls(username, email, password, starting_budget, savings, incomes, expenses)
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
                password TEXT
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS budgets(
                id INTEGER PRIMARY KEY,
                user_email TEXT,
                starting_budget REAL,
                savings REAL,
                FOREIGN KEY(user_email) REFERENCES users(email) ON DELETE CASCADE
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS incomes(
                id INTEGER PRIMARY KEY,
                budget_id INTEGER,
                title TEXT,
                amount REAL,
                date TEXT,
                category TEXT,
                FOREIGN KEY(budget_id) REFERENCES budgets(id) ON DELETE CASCADE
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY,
                budget_id INTEGER,
                title TEXT,
                amount REAL,
                date TEXT,
                category TEXT,
                FOREIGN KEY(budget_id) REFERENCES budgets(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def add_user(self, user_obj):
        with self.conn:
            self.c.execute('INSERT INTO users(username, email, password) VALUES(:username, :email, :password)',
                           {'username': user_obj.username, 'email': user_obj.email, 'password': user_obj.password})
            user_id = self.c.lastrowid
            self.c.execute('INSERT INTO budgets(user_email, starting_budget, savings) VALUES(:user_email, :starting_budget, :savings)',
                           {'user_email': user_obj.email, 'starting_budget': user_obj.starting_budget, 'savings': user_obj.savings})
        self.conn.commit()

    def add_income(self, budget_id, title, amount, date, category, recurring=False):
        with self.conn:
            self.c.execute('INSERT INTO incomes(budget_id, title, amount, date, category, recurring) VALUES(?,?,?,?,?,?)',
                            (budget_id, title, amount, date, category, recurring))
        self.conn.commit()

    def add_expense(self, budget_id, title, amount, date, category, recurring=False):
        with self.conn:
            self.c.execute('INSERT INTO expenses(budget_id, title, amount, date, category, recurring) VALUES(?,?,?,?,?,?)',
                            (budget_id, title, amount, date, category, recurring))
        self.conn.commit()
    
    def get_starting_budget(self, email):
        with self.conn:
            self.c.execute('SELECT starting_budget FROM budgets JOIN users ON users.email = budgets.user_email WHERE users.email = :email', {'email': email})
            result = self.c.fetchone()
            if result is not None:
                return result[0]
            else:
                return None
            
    def get_savings(self, email):
        with self.conn:
            self.c.execute('SELECT savings FROM budgets JOIN users ON users.email = budgets.user_email WHERE users.email = :email', {'email': email})
            result = self.c.fetchone()
            if result is not None:
                return result[0]
            else:
                return None
            
    def get_incomes(self, email):
        with self.conn:
            self.c.execute('SELECT title, amount, date, category FROM incomes JOIN budgets ON budgets.id = incomes.budget_id JOIN users ON users.email = budgets.user_email WHERE users.email = :email',
                           {'email': email})
            return self.c.fetchall()
        
    def get_expenses(self, email):
        with self.conn:
            self.c.execute('SELECT title, amount, date, category FROM expenses JOIN budgets ON budgets.id = expenses.budget_id JOIN users ON users.email = budgets.user_email WHERE users.email = :email',
                           {'email': email})
            return self.c.fetchall()

    def update_entry(self, user):
        conn = sqlite3.connect("data/financly.db")
        c = conn.cursor()

        c.execute("UPDATE users SET starting_budget = ? WHERE email = ?", (user.starting_budget, user.email))

        conn.commit()
        conn.close()

    def select_by_email(self, email):
        with self.conn:
            self.c.execute('SELECT * FROM users WHERE email = (:email)',
                           {'email' : email})
            return self.c.fetchone()
    
    def __del__(self):
        self.conn.close()