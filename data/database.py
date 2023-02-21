import sqlite3

class User():
	
    def add_username(self, username):
        self.username = username
        
    def add_email(self, email):
        self.email = email
    
    def add_password(self, password):
        self.password = password

class Database():
    
    def __init__(self): 
        self.conn = sqlite3.connect('data/financly.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS users(
            username text,
            email text,
            password text)
        ''')
        self.conn.commit()
    
    def add_entry(self, user_obj):
        with self.conn:
            self.c.execute('INSERT INTO users VALUES(:username, :email, :password)',
                      ({'username' : user_obj.username, 
                        'email' : user_obj.email, 
                        'password' : user_obj.password})
            )
        self.conn.commit()
    
    def select_by_email(self, user_obj = None, email = None):
        conn = sqlite3.connect('data/financly.db')
        c = conn.cursor()
        if user_obj is not None:
            with conn:
                c.execute('SELECT * from users where email = (:email)',({'email' : user_obj.email}))
                return c.fetchone()
        else:
            with conn:
                c.execute('SELECT * from users where email = (:email)', ({'email' : email}))
                return c.fetchone()