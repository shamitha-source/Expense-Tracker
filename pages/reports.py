import tkinter as tk
from tkinter import ttk
from datetime import datetime
from database.expense_repository import get_monthly_report

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def show_reports(parent):

    # Clear Page
    for widget in parent.winfo_children():
        widget.destroy()

    parent.configure(bg="#F4F6F9")

    current_date = datetime.now()

    # ---------------- Heading ----------------

    heading = tk.Label(
        parent,
        text="Reports",
        font=("Arial", 24, "bold"),
        bg="#F4F6F9"
    )
    heading.pack(pady=20)

    # ---------------- Month & Year ----------------

    top_frame = tk.Frame(parent, bg="#F4F6F9")
    top_frame.pack(fill="x", padx=30)

    tk.Label(
        top_frame,
        text="Month",
        font=("Arial",12),
        bg="#F4F6F9"
    ).pack(side="left")

    month_combo = ttk.Combobox(
        top_frame,
        values=[
            "January","February","March","April",
            "May","June","July","August",
            "September","October","November","December"
        ],
        state="readonly",
        width=15
    )

    month_combo.current(current_date.month-1)
    month_combo.pack(side="left", padx=10)

    tk.Label(
        top_frame,
        text="Year",
        font=("Arial",12),
        bg="#F4F6F9"
    ).pack(side="left", padx=(20,0))

    year_combo = ttk.Combobox(
        top_frame,
        values=[
            "2024",
            "2025",
            "2026",
            "2027",
            "2028",
            "2029",
            "2030"
        ],
        state="readonly",
        width=10
    )

    year_combo.set(str(current_date.year))
    year_combo.pack(side="left", padx=10)

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

    # ---------------- Summary ----------------

    summary_frame = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )

    summary_frame.pack(
        padx=30,
        pady=20,
        fill="x"
    )

    tk.Label(
        summary_frame,
        text="Monthly Summary",
        font=("Arial",16,"bold"),
        bg="white"
    ).pack(pady=15)

    total_expense_label = tk.Label(
        summary_frame,
        text="Total Expense : ₹0.00",
        font=("Arial",12),
        bg="white"
    )
    total_expense_label.pack(anchor="w", padx=20, pady=5)

    transaction_label = tk.Label(
        summary_frame,
        text="Transactions : 0",
        font=("Arial",12),
        bg="white"
    )
    transaction_label.pack(anchor="w", padx=20, pady=(5,15))

    # ---------------- Pie Chart ----------------

    pie_frame = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )

    pie_frame.pack(
        padx=30,
        pady=10,
        fill="x"
    )

    tk.Label(
        pie_frame,
        text="Expense Distribution",
        font=("Arial",16,"bold"),
        bg="white"
    ).pack(pady=15)

    chart_frame = tk.Frame(
        pie_frame,
        bg="white"
    )

    chart_frame.pack(fill="both", expand=True, pady=10)

    # ---------------- Category Summary ----------------

    table_frame = tk.Frame(
        parent,
        bg="white",
        bd=1,
        relief="solid"
    )

    table_frame.pack(
        padx=30,
        pady=20,
        fill="both",
        expand=True
    )

    tk.Label(
        table_frame,
        text="Category Summary",
        font=("Arial",16,"bold"),
        bg="white"
    ).pack(pady=15)

    columns = (
        "Category",
        "Amount"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=8
    )

    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Amount")

    tree.column(
        "Category",
        width=250,
        anchor="center"
    )

    tree.column(
        "Amount",
        width=250,
        anchor="center"
    )

    tree.pack(
        padx=20,
        pady=10,
        fill="both",
        expand=True
    )

        # ---------------- Load Report ----------------

    def load_report():

        # Clear old table rows
        for row in tree.get_children():
            tree.delete(row)

        # Clear old chart
        for widget in chart_frame.winfo_children():
            widget.destroy()

        month_name = month_combo.get()
        month = month_numbers[month_name]
        year = int(year_combo.get())

        print("Selected:", month_name, year)

        report = get_monthly_report(month, year)

        print("Report:", report)

        # If no data
        if not report:
            total_expense_label.config(
                text="Total Expense : ₹0.00"
            )

            transaction_label.config(
                text="Transactions : 0"
            )

            tk.Label(
                chart_frame,
                text="No expenses found for selected month.",
                bg="white",
                fg="gray",
                font=("Arial",12)
            ).pack(pady=40)

            return


        # Total Expense
        total = sum(amount for category, amount in report)

        total_expense_label.config(
            text=f"Total Expense : ₹{total:.2f}"
        )

        transaction_label.config(
            text=f"Transactions : {len(report)}"
        )


        # Category-wise Total
        category_totals = {}

        for category, amount in report:
            category_totals[category] = category_totals.get(category,0)+amount


        # Fill Table
        for category, amount in category_totals.items():
            tree.insert(
                "",
                "end",
                values=(category, f"₹{amount:.2f}")
            )


        # Pie Chart
        figure = Figure(figsize=(7,4), dpi=100)

        ax = figure.add_subplot(111)

        wedges, _ = ax.pie(
            list(category_totals.values()),
            startangle=90
        )


        legend_labels=[]

        for category, amount in category_totals.items():

            percentage=(amount/total)*100

            legend_labels.append(
                f"{category} ₹{amount:.2f} ({percentage:.1f}%)"
            )


        ax.legend(
            wedges,
            legend_labels,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1,0.5)
        )

        ax.set_title("Expense Distribution")


        canvas = FigureCanvasTkAgg(
            figure,
            master=chart_frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    # Bind only once (outside load_report)

    month_combo.bind(
        "<<ComboboxSelected>>",
        lambda event: load_report()
    )


    year_combo.bind(
        "<<ComboboxSelected>>",
        lambda event: load_report()
    )


    # Initial Load
    load_report()   
   