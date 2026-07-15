import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database.expense_repository import add_expense
from pages.dashboard import show_dashboard


def show_add_expense(parent, expense=None):

    # Clear previous page
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="#F4F6F9")

    # ===================== Heading =====================

    heading = tk.Label(
        parent,
        text="Add Expense",
        font=("Arial", 22, "bold"),
        bg="#F4F6F9"
    )
    heading.pack(pady=20)

    # ===================== Form =====================

    form_frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
    form_frame.pack(padx=30, pady=20)

    # Date
    tk.Label(
        form_frame,
        text="Date",
        bg="white",
        font=("Arial", 11)
    ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

    date_entry = DateEntry(
        form_frame,
        width=25,
        date_pattern="dd-mm-yyyy"
    )
    date_entry.grid(row=0, column=1, padx=20, pady=15)

    # Category
    tk.Label(
        form_frame,
        text="Category",
        bg="white",
        font=("Arial", 11)
    ).grid(row=1, column=0, padx=20, pady=15, sticky="w")

    category = ttk.Combobox(
        form_frame,
        values=[
            "Groceries",
            "Rent",
            "Travel",
            "Shopping",
            "Bills",
            "Food",
            "Entertainment",
            "Others"
        ],
        state="readonly",
        width=23
    )
    category.grid(row=1, column=1, padx=20)

    # Amount
    tk.Label(
        form_frame,
        text="Amount (₹)",
        bg="white",
        font=("Arial", 11)
    ).grid(row=2, column=0, padx=20, pady=15, sticky="w")

    amount_entry = tk.Entry(form_frame, width=27)
    amount_entry.grid(row=2, column=1, padx=20)

    # Description
    tk.Label(
        form_frame,
        text="Description",
        bg="white",
        font=("Arial", 11)
    ).grid(row=3, column=0, padx=20, pady=15, sticky="w")

    description_entry = tk.Entry(form_frame, width=27)
    description_entry.grid(row=3, column=1, padx=20)

    # Payment Method
    tk.Label(
        form_frame,
        text="Payment Method",
        bg="white",
        font=("Arial", 11)
    ).grid(row=4, column=0, padx=20, pady=15, sticky="w")

    payment = ttk.Combobox(
        form_frame,
        values=["Cash", "UPI", "Card"],
        state="readonly",
        width=23
    )
    payment.grid(row=4, column=1, padx=20)

    # ===================== Save Function =====================

    def save_expense():

        expense_date = date_entry.get()
        expense_category = category.get()
        expense_amount = amount_entry.get()
        expense_description = description_entry.get()
        payment_method = payment.get()

        if expense_category == "" or expense_amount == "" or payment_method == "":
            messagebox.showerror(
                "Error",
                "Please fill all required fields."
            )
            return

        try:
            amount = float(expense_amount)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be a number."
            )
            return

        add_expense(
            expense_date,
            expense_category,
            amount,
            expense_description,
            payment_method
        )

        messagebox.showinfo(
            "Success",
            "Expense added successfully."
        )

        show_dashboard(parent)

    # ===================== Button =====================

    tk.Button(
        form_frame,
        text="Add Expense",
        bg="#2E8B57",
        fg="white",
        font=("Arial", 11, "bold"),
        width=18,
        command=save_expense
    ).grid(row=5, column=0, columnspan=2, pady=20)