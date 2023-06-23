import sqlite3

def create_connection():
    connection = sqlite3.connect("brain.db")
    return connection

def get_table():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM question_answers")
    return cursor.fetchall()

def get_questions_answers():
    """
    Fetch all rows from the question_answers table in the database, and return them as a list.
    
    Returns:
    list: a list of rows in the question_answers table
    """
    rows = get_table()
    bot_list = []
    for row in rows:
        bot_list.extend(list(row))
    return bot_list