import sqlite3

def create_connection(db_file):
    # Создает подключение к базе данных SQLite
    # :param  db_file: путь к файлу базы данных
    # return:  объект соединения или None
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)
        return conn

