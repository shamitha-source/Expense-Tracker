from database import get_connection


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Expenses Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            payment_method TEXT
        )
    """)


    # Budget Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            amount REAL NOT NULL
        )
    """)


    connection.commit()
    connection.close()


if __name__ == "__main__":
    create_tables()
    print("Database, Expenses and Budget tables created successfully.")