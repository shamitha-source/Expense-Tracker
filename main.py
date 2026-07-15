import tkinter as tk
from pages.dashboard import show_dashboard
from pages.add_expense import show_add_expense
from pages.history import show_history
from pages.reports import show_reports
from pages.budget import show_budget
root = tk.Tk()

root.title("Expense Tracker")
root.geometry("1200x700")
root.resizable(False, False)

# ================= Sidebar =================

sidebar = tk.Frame(root, bg="#2C3E50", width=250)
sidebar.pack(side="left", fill="y")

title = tk.Label(
    sidebar,
    text="Expense Tracker",
    bg="#2C3E50",
    fg="white",
    font=("Arial", 18, "bold")
)
title.pack(pady=30)

dashboard_btn = tk.Button(
    sidebar,
    text="Dashboard",
    font=("Arial", 12),
    bg="#34495E",
    fg="white",
    relief="flat",
    width=20,
    height=2,
    command=lambda: show_dashboard(content)
)
dashboard_btn.pack(pady=8)

add_expense_btn = tk.Button(
    sidebar,
    text="Add Expense",
    font=("Arial", 12),
    bg="#34495E",
    fg="white",
    relief="flat",
    width=20,
    height=2,
    command=lambda: show_add_expense(content)
)
add_expense_btn.pack(pady=8)

history_btn = tk.Button(
    sidebar,
    text="History",
    font=("Arial", 12),
    bg="#34495E",
    fg="white",
    relief="flat",
    width=20,
    height=2,
    command=lambda: show_history(content)
)
history_btn.pack(pady=8)

reports_btn = tk.Button(
    sidebar,
    text="Reports",
    font=("Arial", 12),
    bg="#34495E",
    fg="white",
    relief="flat",
    width=20,
    height=2,
 command=lambda: show_reports(content)   
)
reports_btn.pack(pady=8)

budget_btn = tk.Button(
    sidebar,
    text="Budget",
    font=("Arial", 12),
    bg="#34495E",
    fg="white",
    relief="flat",
    width=20,
    height=2,
    command=lambda: show_budget(content)
)
budget_btn.pack(pady=8)


# ================= Main Content =================

content = tk.Frame(root, bg="white")
content.pack(side="right", fill="both", expand=True)

show_dashboard(content)

root.mainloop()