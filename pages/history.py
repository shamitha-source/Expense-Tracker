import tkinter as tk
from tkinter import messagebox
from database.expense_repository import (
    get_expenses_grouped_by_date,
    delete_expense,
    get_expense_by_id
)

from pages.add_expense import show_add_expense


def show_history(parent):

    # Clear page
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="#F4F6F9")

    # Heading
    heading = tk.Label(
        parent,
        text="Expense History",
        font=("Arial", 22, "bold"),
        bg="#F4F6F9"
    )
    heading.pack(pady=20)

    # Scroll Area
    canvas = tk.Canvas(parent, bg="#F4F6F9", highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)

    scroll_frame = tk.Frame(canvas, bg="#F4F6F9")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    def _on_mousewheel(event):
     canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    grouped = get_expenses_grouped_by_date()

    if not grouped:
        tk.Label(
            scroll_frame,
            text="No expenses found.",
            font=("Arial", 14),
            bg="#F4F6F9"
        ).pack(pady=40)
        return

    icons = {
        "Groceries": "🥦",
        "Rent": "🏠",
        "Travel": "🚌",
        "Shopping": "🛍",
        "Bills": "💡",
        "Food": "🍕",
        "Entertainment": "🎬",
        "Others": "📦"
    }

    def refresh():
        show_history(parent)
        

    for expense_date, expenses in grouped.items():

        card = tk.Frame(
            scroll_frame,
            bg="white",
            bd=1,
            relief="solid"
        )
        card.pack(fill="x", padx=20, pady=10)

        tk.Label(
            card,
            text=f"📅 {expense_date}",
            font=("Arial", 15, "bold"),
            bg="white"
        ).pack(anchor="w", padx=15, pady=(12, 8))

        total = 0

        for expense in expenses:

            total += expense["amount"]

            row = tk.Frame(card, bg="white")
            row.pack(fill="x", padx=20, pady=5)

            icon = icons.get(expense["category"], "📦")

            left = tk.Frame(row, bg="white")
            left.pack(side="left")

            tk.Label(
                left,
                text=f"{icon} {expense['category']}",
                bg="white",
                font=("Arial", 11, "bold")
            ).pack(anchor="w")

            if expense["description"]:
                tk.Label(
                    left,
                    text=expense["description"],
                    bg="white",
                    fg="gray",
                    font=("Arial", 10)
                ).pack(anchor="w")

            tk.Label(
                row,
                text=f"₹ {expense['amount']}",
                bg="white",
                fg="#2E8B57",
                font=("Arial", 11, "bold")
            ).pack(side="right")

            button_frame = tk.Frame(card, bg="white")
            button_frame.pack(anchor="e", padx=20)

            tk.Button(
                button_frame,
                text="🗑 Delete",
                bg="#E74C3C",
                fg="white",
                relief="flat",
                command=lambda eid=expense["id"]: delete_item(eid)
            ).pack(side="right", padx=5)

        tk.Frame(card, bg="#DDDDDD", height=1).pack(fill="x", padx=15, pady=10)

        tk.Label(
            card,
            text=f"💰 Daily Total : ₹ {total}",
            bg="white",
            fg="#2E8B57",
            font=("Arial", 12, "bold")
        ).pack(anchor="e", padx=15, pady=(0, 12))

    def delete_item(expense_id):

        answer = messagebox.askyesno(
            "Delete Expense",
            "Are you sure you want to delete this expense?"
        )

        if answer:
            delete_expense(expense_id)
            refresh()