import sqlite3
import os

DATABASE_NAME = "expenses.db"

DATABASE_PATH = os.path.join(os.path.dirname(__file__), DATABASE_NAME)


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    return connection