from datetime import datetime
from database.database import get_connection

def add_expense(expense_date, category, amount, description, payment_method):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (expense_date, category, amount, description, payment_method)
        VALUES (?, ?, ?, ?, ?)
    """, (expense_date, category, amount, description, payment_method))

    connection.commit()
    connection.close()


def get_all_expenses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id,
               expense_date,
               category,
               amount,
               description,
               payment_method
        FROM expenses
        ORDER BY expense_date DESC
    """)

    data = cursor.fetchall()

    connection.close()

    return data


def get_expenses_grouped_by_date():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id,
               expense_date,
               category,
               amount,
               description,
               payment_method
        FROM expenses
        ORDER BY expense_date DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    grouped = {}

    for expense_id, expense_date, category, amount, description, payment in rows:

        if expense_date not in grouped:
            grouped[expense_date] = []

        grouped[expense_date].append({
            "id": expense_id,
            "category": category,
            "amount": amount,
            "description": description,
            "payment": payment
        })

    return grouped


def delete_expense(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id=?",
        (expense_id,)
    )

    connection.commit()
    connection.close()


def get_dashboard_data():

    connection = get_connection()
    cursor = connection.cursor()

    today = datetime.now().strftime("%d-%m-%Y")
    current_month = datetime.now().strftime("%m-%Y")

    # Today's Total
    cursor.execute("""
        SELECT IFNULL(SUM(amount), 0)
        FROM expenses
        WHERE expense_date = ?
    """, (today,))
    today_total = cursor.fetchone()[0]

    # This Month Total
    cursor.execute("""
        SELECT IFNULL(SUM(amount), 0)
        FROM expenses
        WHERE substr(expense_date, 4, 7) = ?
    """, (current_month,))
    month_total = cursor.fetchone()[0]

    # Total Transactions
    cursor.execute("""
        SELECT COUNT(*)
        FROM expenses
    """)
    transactions = cursor.fetchone()[0]

    # Top Spending Category
    cursor.execute("""
        SELECT category,
               SUM(amount) AS total
        FROM expenses
        GROUP BY category
        ORDER BY total DESC
        LIMIT 1
    """)

    result = cursor.fetchone()
    top_category = result[0] if result else "None"

    # Recent 5 Expenses
    cursor.execute("""
        SELECT category,
               amount
        FROM expenses
        ORDER BY id DESC
        LIMIT 5
    """)

    recent = cursor.fetchall()

    connection.close()

    return {
        "today_total": today_total,
        "month_total": month_total,
        "transactions": transactions,
        "top_category": top_category,
        "recent": recent
    }
def get_expense_by_id(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            expense_date,
            category,
            amount,
            description,
            payment_method
        FROM expenses
        WHERE id=?
    """, (expense_id,))

    expense = cursor.fetchone()

    connection.close()

    return expense


def update_expense(expense_id, expense_date, category, amount, description, payment_method):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE expenses
        SET
            expense_date=?,
            category=?,
            amount=?,
            description=?,
            payment_method=?
        WHERE id=?
    """, (
        expense_date,
        category,
        amount,
        description,
        payment_method,
        expense_id
    ))

    connection.commit()

    connection.close()

def get_monthly_report(month, year):

    connection = get_connection()
    cursor = connection.cursor()

    month = str(month).zfill(2)
    year = str(year)

    cursor.execute("""
        SELECT category, amount
        FROM expenses
        WHERE expense_date LIKE ?
    """, (f"%-{month}-{year}",))

    data = cursor.fetchall()

    connection.close()
    print("Query month:", month)
    print("Query year:", year)
    print("Result:", data)
    return data
def save_budget(month, year, amount):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM budget
        WHERE month=? AND year=?
    """,(month,year))


    cursor.execute("""
        INSERT INTO budget(month,year,amount)
        VALUES(?,?,?)
    """,(month,year,amount))


    connection.commit()
    connection.close()



def get_budget(month, year):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT amount
        FROM budget
        WHERE month=? AND year=?
    """,(month,year))


    data = cursor.fetchone()

    connection.close()

    if data:
        return data[0]

    return 0