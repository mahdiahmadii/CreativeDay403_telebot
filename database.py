import sqlite3
import os
from datetime import datetime

# Database connection
def get_db_connection():
    # Create database directory if it doesn't exist
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect('database/database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database and create tables
def initialize_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        chat_id INTEGER NOT NULL,
        profile_name TEXT,
        fname TEXT,
        lname TEXT,
        stunumber TEXT UNIQUE CHECK(length(stunumber) BETWEEN 6 AND 10),
        personality_number TEXT UNIQUE,
        administration INTEGER DEFAULT 0 CHECK(administration IN (0, 1, 2)),
        number_of_messages INTEGER DEFAULT 0,
        allowing BOOLEAN DEFAULT TRUE
    )
    ''')
    
    # Create Messages table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Messages (
        message_id INTEGER PRIMARY KEY,
        message_subject TEXT,
        chat_id INTEGER,
        user_id INTEGER,
        dateAndTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_answered BOOLEAN DEFAULT FALSE,
        is_seened BOOLEAN DEFAULT FALSE,
        type_of_message TEXT,
        message_content TEXT,
        ans_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')
    
    conn.commit()
    conn.close()

# [Rest of your functions remain exactly the same as in the original code...]
# User management functions
def add_new_user(user_id, chat_id, profile_name, administration=0, messages_count=0):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Users (user_id, chat_id, profile_name, administration, number_of_messages)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, chat_id, profile_name, administration, messages_count))
    
    conn.commit()
    conn.close()

def register_user(user_id, lname, fname, stu_number, personality_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE Users 
    SET lname = ?, fname = ?, stunumber = ?, personality_number = ?
    WHERE user_id = ?
    ''', (lname, fname, stu_number, personality_code, user_id))
    
    conn.commit()
    conn.close()

def update_user_information(user_id, lname=None, fname=None, stu_number=None, personality_code=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build dynamic update query based on provided parameters
    updates = []
    params = []
    
    if lname is not None:
        updates.append("lname = ?")
        params.append(lname)
    if fname is not None:
        updates.append("fname = ?")
        params.append(fname)
    if stu_number is not None:
        updates.append("stunumber = ?")
        params.append(stu_number)
    if personality_code is not None:
        updates.append("personality_number = ?")
        params.append(personality_code)
    
    if updates:
        query = "UPDATE Users SET " + ", ".join(updates) + " WHERE user_id = ?"
        params.append(user_id)
        cursor.execute(query, params)
    
    conn.commit()
    conn.close()



def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    conn.close()
    return user




def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()

# Message management functions
def add_message(message_id, subject, chat_id, user_id, answered=False, seened=False, type_of_message=None, message_content=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Messages (message_id, message_subject, chat_id, user_id, is_answered, is_seened, type_of_message, message_content)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (message_id, subject, chat_id, user_id, answered, seened, type_of_message, message_content))
    
    # Increment user's message count
    cursor.execute('''
    UPDATE Users 
    SET number_of_messages = number_of_messages + 1
    WHERE user_id = ?
    ''', (user_id,))
    
    conn.commit()
    conn.close()

def delete_message(message_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM Messages WHERE message_id = ?', (message_id,))
    
    conn.commit()
    conn.close()

def is_answered(message_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE Messages SET is_answered = TRUE WHERE message_id = ?', (message_id,))
    
    conn.commit()
    conn.close()

def is_seened(message_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE Messages SET is_seened = TRUE WHERE message_id = ?', (message_id,))
    
    conn.commit()
    conn.close()

# Administration functions
def promote(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE Users SET administration = 1 WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()

def unpromote(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE Users SET administration = 0 WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()

def ban(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE Users SET allowing = FALSE WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()

def unban(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE Users SET allowing = TRUE WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()

# Selection functions
def select_all_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Messages ORDER BY dateAndTime DESC')
    messages = cursor.fetchall()
    
    conn.close()
    return messages

def select_all_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    
    conn.close()
    return users

def select_simple_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Users WHERE administration = 0')
    users = cursor.fetchall()
    
    conn.close()
    return users

def select_admins():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Users WHERE administration > 0')
    admins = cursor.fetchall()
    
    conn.close()
    return admins

def select_last20_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Messages where is_answered = 0 ORDER BY dateAndTime DESC LIMIT 20')
    messages = cursor.fetchall()
    
    conn.close()
    return messages

def show_message_subjective(subject):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Messages WHERE message_subject = ? ORDER BY dateAndTime DESC', (subject,))
    messages = cursor.fetchall()
    
    conn.close()
    return messages

def select_chat_user(chat_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Messages WHERE chat_id = ? ORDER BY dateAndTime DESC', (chat_id,))
    messages = cursor.fetchall()
    
    conn.close()
    return messages

# Initialize the database when this module is imported
initialize_database()