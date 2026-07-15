import tkinter as tk
from database.expense_repository import get_dashboard_data


def show_dashboard(parent):

    # Clear page
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="#F4F6F9")

    data = get_dashboard_data()

    # ================= Heading =================

    heading = tk.Label(
        parent,
        text="Expense Tracker Dashboard",
        font=("Arial", 24, "bold"),
        bg="#F4F6F9"
    )
    heading.pack(pady=20)

    # ================= Cards =================

    cards_frame = tk.Frame(parent, bg="#F4F6F9")
    cards_frame.pack(pady=10)

    def create_card(row, column, title, value):

        card = tk.Frame(
            cards_frame,
            bg="white",
            width=220,
            height=110,
            bd=1,
            relief="solid"
        )

        card.grid(row=row, column=column, padx=20, pady=15)
        card.grid_propagate(False)

        tk.Label(
            card,
            text=title,
            bg="white",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        tk.Label(
            card,
            text=value,
            bg="white",
            fg="#2E8B57",
            font=("Arial", 20, "bold")
        ).pack()

    create_card(
        0,
        0,
        "Today's Expense",
        f"₹ {data['today_total']}"
    )

    create_card(
        0,
        1,
        "This Month",
        f"₹ {data['month_total']}"
    )

    create_card(
        1,
        0,
        "Transactions",
        str(data["transactions"])
    )

    create_card(
        1,
        1,
        "Top Category",
        data["top_category"]
    )

    # ================= Recent Expenses =================

    recent_frame = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )

    recent_frame.pack(
        padx=30,
        pady=25,
        fill="both",
        expand=True
    )

    tk.Label(
        recent_frame,
        text="Recent Expenses",
        bg="white",
        font=("Arial", 16, "bold")
    ).pack(anchor="w", padx=20, pady=15)

    if len(data["recent"]) == 0:

        tk.Label(
            recent_frame,
            text="No expenses added yet.",
            bg="white",
            fg="gray",
            font=("Arial", 12)
        ).pack(pady=20)

    else:

        for category, amount in data["recent"]:

            row = tk.Frame(
                recent_frame,
                bg="white"
            )
            row.pack(fill="x", padx=20, pady=5)

            tk.Label(
                row,
                text=category,
                bg="white",
                font=("Arial", 11)
            ).pack(side="left")

            tk.Label(
                row,
                text=f"₹ {amount}",
                bg="white",
                fg="#2E8B57",
                font=("Arial", 11, "bold")
            ).pack(side="right")