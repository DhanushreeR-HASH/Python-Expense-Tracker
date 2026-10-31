import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

FILE_NAME = "expenses.csv"


class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        self.root.geometry("700x550")

        self.expenses = []

        self.load_expenses()
        self.create_widgets()
        self.update_table()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="PERSONAL EXPENSE TRACKER",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=15)

        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Description").grid(row=0, column=0)
        tk.Label(form, text="Category").grid(row=0, column=1)
        tk.Label(form, text="Amount (₹)").grid(row=0, column=2)

        self.description = tk.Entry(form, width=20)
        self.description.grid(row=1, column=0, padx=5)

        self.category = ttk.Combobox(
            form,
            values=[
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Bills",
                "Other"
            ],
            width=17,
            state="readonly"
        )
        self.category.grid(row=1, column=1, padx=5)
        self.category.set("Food")

        self.amount = tk.Entry(form, width=15)
        self.amount.grid(row=1, column=2, padx=5)

        tk.Button(
            form,
            text="Add Expense",
            command=self.add_expense,
            bg="green",
            fg="white"
        ).grid(row=2, column=0, columnspan=3, pady=15)

        columns = ("Description", "Category", "Amount")

        self.table = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings",
            height=12
        )

        for column in columns:
            self.table.heading(column, text=column)

        self.table.pack(pady=10, padx=20, fill="both", expand=True)

        self.total_label = tk.Label(
            self.root,
            text="Total Expenses: ₹0.00",
            font=("Arial", 14, "bold")
        )
        self.total_label.pack(pady=10)

        tk.Button(
            self.root,
            text="Delete Selected Expense",
            command=self.delete_expense,
            bg="red",
            fg="white"
        ).pack(pady=10)

    def add_expense(self):

        description = self.description.get().strip()
        category = self.category.get()
        amount = self.amount.get().strip()

        if not description or not amount:
            messagebox.showerror(
                "Error",
                "Please enter all details."
            )
            return

        try:
            amount = float(amount)

            if amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter a valid positive amount."
            )
            return

        expense = {
            "description": description,
            "category": category,
            "amount": amount
        }

        self.expenses.append(expense)

        self.save_expenses()
        self.update_table()

        self.description.delete(0, tk.END)
        self.amount.delete(0, tk.END)

    def update_table(self):

        for item in self.table.get_children():
            self.table.delete(item)

        total = 0

        for expense in self.expenses:

            self.table.insert(
                "",
                tk.END,
                values=(
                    expense["description"],
                    expense["category"],
                    f"₹{expense['amount']:.2f}"
                )
            )

            total += expense["amount"]

        self.total_label.config(
            text=f"Total Expenses: ₹{total:.2f}"
        )

    def save_expenses(self):

        with open(FILE_NAME, "w", newline="") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=["description", "category", "amount"]
            )

            writer.writeheader()
            writer.writerows(self.expenses)

    def load_expenses(self):

        if os.path.exists(FILE_NAME):

            with open(FILE_NAME, "r", newline="") as file:

                reader = csv.DictReader(file)

                for row in reader:

                    self.expenses.append({
                        "description": row["description"],
                        "category": row["category"],
                        "amount": float(row["amount"])
                    })

    def delete_expense(self):

        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning",
                "Select an expense to delete."
            )
            return

        index = self.table.index(selected[0])

        del self.expenses[index]

        self.save_expenses()
        self.update_table()


root = tk.Tk()
app = ExpenseTracker(root)
root.mainloop()
