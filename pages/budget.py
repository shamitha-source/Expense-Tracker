import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.database import get_connection

def show_budget(parent):

    # Clear Page
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="#F4F6F9")

    current_date = datetime.now()


    # ---------------- Heading ----------------

    heading = tk.Label(
        parent,
        text="Budget",
        font=("Arial", 24, "bold"),
        bg="#F4F6F9"
    )

    heading.pack(pady=20)



    # ---------------- Month Year ----------------

    top_frame = tk.Frame(
        parent,
        bg="#F4F6F9"
    )

    top_frame.pack(pady=10)


    months = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]


    month_numbers = {
        "January":1,
        "February":2,
        "March":3,
        "April":4,
        "May":5,
        "June":6,
        "July":7,
        "August":8,
        "September":9,
        "October":10,
        "November":11,
        "December":12
    }


    tk.Label(
        top_frame,
        text="Month",
        bg="#F4F6F9",
        font=("Arial",12)
    ).pack(side="left")


    month_combo = ttk.Combobox(
        top_frame,
        values=months,
        state="readonly",
        width=15
    )

    month_combo.current(current_date.month-1)
    month_combo.pack(side="left", padx=10)



    tk.Label(
        top_frame,
        text="Year",
        bg="#F4F6F9",
        font=("Arial",12)
    ).pack(side="left")


    year_combo = ttk.Combobox(
        top_frame,
        values=[
            "2024","2025","2026",
            "2027","2028","2029","2030"
        ],
        state="readonly",
        width=10
    )

    year_combo.set(str(current_date.year))
    year_combo.pack(side="left", padx=10)



    # ---------------- Set Budget ----------------


    budget_frame = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )

    budget_frame.pack(
        padx=30,
        pady=20,
        fill="x"
    )


    tk.Label(
        budget_frame,
        text="Set Monthly Budget",
        font=("Arial",16,"bold"),
        bg="white"
    ).pack(pady=15)



    amount_entry = tk.Entry(
        budget_frame,
        font=("Arial",12),
        width=20
    )

    amount_entry.pack(pady=10)



    # ---------------- Summary ----------------


    summary_frame = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )

    summary_frame.pack(
        padx=30,
        pady=10,
        fill="x"
    )


    budget_label = tk.Label(
        summary_frame,
        text="Budget : ₹0.00",
        font=("Arial",13),
        bg="white"
    )

    budget_label.pack(pady=5)


    spent_label = tk.Label(
        summary_frame,
        text="Spent : ₹0.00",
        font=("Arial",13),
        bg="white"
    )

    spent_label.pack(pady=5)


    remaining_label = tk.Label(
        summary_frame,
        text="Remaining : ₹0.00",
        font=("Arial",13),
        bg="white"
    )

    remaining_label.pack(pady=5)

    exceeded_label = tk.Label(
    summary_frame,
    text="Exceeded : ₹0.00",
    font=("Arial",13),
    bg="white"
)

    exceeded_label.pack(pady=5)



    progress = ttk.Progressbar(
        summary_frame,
        length=400,
        mode="determinate"
    )

    progress.pack(pady=15)



    # ---------------- Database Functions ----------------


    def save_budget():

        month = month_numbers[month_combo.get()]
        year = int(year_combo.get())

        try:
            amount = float(amount_entry.get())

        except:
            messagebox.showerror(
                "Error",
                "Enter valid budget amount"
            )
            return


        connection = get_connection()
        cursor = connection.cursor()


        cursor.execute("""
            DELETE FROM budget
            WHERE month=? AND year=?
        """,
        (month,year))


        cursor.execute("""
            INSERT INTO budget(month,year,amount)
            VALUES(?,?,?)
        """,
        (month,year,amount))


        connection.commit()
        connection.close()


        messagebox.showinfo(
            "Success",
            "Budget saved successfully"
        )


        load_budget()



    def fetch_budget(month,year):

        connection = get_connection()
        cursor = connection.cursor()


        cursor.execute("""
            SELECT amount
            FROM budget
            WHERE month=? AND year=?
        """,
        (month,year))


        result = cursor.fetchone()

        connection.close()


        if result:
            return result[0]

        return 0



    def fetch_expense(month,year):

        connection = get_connection()
        cursor = connection.cursor()


        cursor.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE substr(expense_date,4,2)=?
            AND substr(expense_date,7,4)=?
        """,
        (
            str(month).zfill(2),
            str(year)
        ))


        result = cursor.fetchone()

        connection.close()


        if result[0]:
            return result[0]

        return 0



    def load_budget():

        month = month_numbers[month_combo.get()]
        year = int(year_combo.get())


        budget = fetch_budget(
            month,
            year
        )


        spent = fetch_expense(
            month,
            year
        )


        remaining = budget - spent



        budget_label.config(
            text=f"Budget : ₹{budget:.2f}"
        )


        spent_label.config(
            text=f"Spent : ₹{spent:.2f}"
        )


        if remaining >= 0:

           remaining_label.config(
               text=f"Remaining : ₹{remaining:.2f}"
            )

           exceeded_label.config(
             text="Exceeded : ₹0.00"
            )

        else:

           remaining_label.config(
              text="Remaining : ₹0.00"
            )

           exceeded_label.config(
              text=f"Exceeded : ₹{-remaining:.2f}"
            )


        if budget > 0:

            percentage = (spent / budget) * 100

            progress["value"] = min(
                percentage,
                100
            )

        else:

            progress["value"] = 0



    # ---------------- Button ----------------


    save_button = tk.Button(
        budget_frame,
        text="Save Budget",
        command=save_budget,
        font=("Arial",12),
        bg="#4CAF50",
        fg="white"
    )

    save_button.pack(pady=10)



    # ---------------- Events ----------------

    month_combo.bind(
        "<<ComboboxSelected>>",
        lambda event: load_budget()
    )


    year_combo.bind(
        "<<ComboboxSelected>>",
        lambda event: load_budget()
    )


    load_budget()