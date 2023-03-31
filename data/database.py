import sqlite3

class User():
    def __init__(self, username=None, email=None, password=None, starting_budget=None, savings=None):
        self.username = username
        self.email = email
        self.password = password
        self.starting_budget = starting_budget
        self.savings = savings
        
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


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data/financly.db')
        self.c = self.conn.cursor()
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
                user_id INTEGER,
                starting_budget REAL,
                savings REAL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def add_user(self, user_obj):
        with self.conn:
            self.c.execute('INSERT INTO users(username, email, password) VALUES(:username, :email, :password)',
                           {'username': user_obj.username, 'email': user_obj.email, 'password': user_obj.password})
            user_id = self.c.lastrowid
            self.c.execute('INSERT INTO budgets(user_id, starting_budget, savings) VALUES(:user_id, :starting_budget, :savings)',
                           {'user_id': user_id, 'starting_budget': user_obj.starting_budget, 'savings': user_obj.savings})
        self.conn.commit()
        
    def get_starting_budget(self, email):
        with self.conn:
            self.c.execute('SELECT starting_budget FROM budgets JOIN users ON users.id = budgets.user_id WHERE users.email = :email', {'email': email})
            return self.c.fetchone()[0]
        
    def update_starting_budget(self, email, starting_budget):
        with self.conn:
            self.c.execute('UPDATE budgets SET starting_budget = :starting_budget WHERE user_id = (SELECT id FROM users WHERE email = :email)',
                           {'starting_budget': starting_budget, 'email': email})
        self.conn.commit()
    
    def select_by_email(self, email):
        with self.conn:
            self.c.execute('SELECT * FROM users WHERE email = (:email)',
                           {'email' : email})
            return self.c.fetchone()
    
    def __del__(self):
        self.conn.close()