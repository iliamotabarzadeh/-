import tkinter as tk
import sqlite3


database = sqlite3.connect("database.db")
cursor = database.cursor()


# Create table when the program starts
cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        amount INTEGER,
        category TEXT,
        description TEXT
    )
""")

database.commit()


window = tk.Tk()
window.title("Personal Finance Manager")
window.geometry("800x500")


def view_transactions():
    view_window = tk.Toplevel(window)
    view_window.title("View Transactions")
    view_window.geometry("500x400")

    cursor.execute("""
                   SELECT id, type, amount, category, description
                   FROM transactions
                   """)
    transactions = cursor.fetchall()

    if not transactions:
        tk.Label(
            view_window,
            text="No transactions found"
        ).pack()

        return

    for transaction in transactions:
        transaction_text = (
            f"ID: {transaction[0]} | "
            f"Type: {transaction[1]} | "
            f"Amount: {transaction[2]} | "
            f"Category: {transaction[3]} | "
            f"Description: {transaction[4]}"
        )
        tk.Label(
            view_window,
            text=transaction_text
        ).pack(anchor="w")

def filter_transactions():
    filter_window = tk.Toplevel(window)
    filter_window.title("Filter Transactions")
    filter_window.geometry("500x400")

    tk.Label(
        filter_window,
        text="Filter Type"
    ).pack()

    filter_var = tk.StringVar()
    filter_var.set("All")

    filter_menu = tk.OptionMenu(
        filter_window,
        filter_var,
        "All",
        "Income",
        "Expense"
    )
    filter_menu.pack()

    results_frame = tk.Frame(filter_window)
    results_frame.pack(fill="both", expand=True)

    def apply_filter():
        selected_type = filter_var.get()

        if selected_type == "All":
            cursor.execute("""
                SELECT type, amount, category, description
                FROM transactions
            """)
        else:
            cursor.execute("""
                SELECT type, amount, category, description
                FROM transactions
                WHERE type = ?
            """, (selected_type,))

        transactions = cursor.fetchall()

        for widget in results_frame.winfo_children():
            widget.destroy()

        if not transactions:
            tk.Label(
                results_frame,
                text="No transactions found"
            ).pack()
            return

        for transaction in transactions:
            transaction_text = (
                f"Type: {transaction[0]} | "
                f"Amount: {transaction[1]} | "
                f"Category: {transaction[2]} | "
                f"Description: {transaction[3]}"
            )

            tk.Label(
                results_frame,
                text=transaction_text
            ).pack(anchor="w")

    filter_button = tk.Button(
        filter_window,
        text="Apply Filter",
        command=apply_filter
    )
    filter_button.pack()


def reset_transactions():
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='transactions'")
    database.commit()
    print("All transactions have been deleted")
def show_balance():
    cursor.execute("""
                   SELECT type, amount
                   FROM transactions
                   """)
    transactions = cursor.fetchall()

    total_Income = 0
    total_Expense = 0
    for transaction in transactions:
        transaction_type = transaction[0]
        amount = int(transaction[1])

        if transaction_type == "Income":
            total_Income += amount
        elif transaction_type == "Expense":
            total_Expense += amount
    balance = total_Income - total_Expense

    balance_window = tk.Toplevel(window)
    balance_window.title("Balance")
    balance_window.geometry("300x200")
    balance_window.configure(background="white")

    tk.Label(
        balance_window,
        text=f"Income: {total_Income:,} "
    ).pack()
    tk.Label(
        balance_window,
        text=f"Expense: {total_Expense:,} "
    ).pack()
    tk.Label(
        balance_window,
        text=f"Balance: {balance:,} "
    ).pack()


def add_transaction():

    add_window = tk.Toplevel(window)
    add_window.title("Add Transaction")
    add_window.geometry("400x300")
    add_window.configure(background="white")


    tk.Label(add_window, text="Amount").pack()

    amount_entry = tk.Entry(add_window)
    amount_entry.pack()


    tk.Label(add_window, text="Type").pack()

    type_var = tk.StringVar()
    type_var.set("Income")

    type_menu = tk.OptionMenu(
        add_window,
        type_var,
        "Income",
        "Expense"
    )

    type_menu.pack()


    tk.Label(add_window, text="Category").pack()

    entry_category = tk.Entry(add_window)
    entry_category.pack()


    tk.Label(add_window, text="Description").pack()

    entry_description = tk.Entry(add_window)
    entry_description.pack()

    error_label = tk.Label(
        add_window,
        text="",
        fg="red"
    )
    error_label.pack()



    def save_transaction():

        amount = amount_entry.get()

        if not amount.isdigit():
            error_label.config(
                text = "Please enter only numbers."
            )
            return

        error_label.config(text="")

        transaction_type = type_var.get()
        category = entry_category.get()
        description = entry_description.get()


        cursor.execute("""
            INSERT INTO transactions
            (type, amount, category, description)
            VALUES (?, ?, ?, ?)
        """, (
            transaction_type,
            amount,
            category,
            description
        ))


        database.commit()

    error_label.config(
        text="Transaction saved successfully",
        fg="green"
    )

    save_button = tk.Button(
        add_window,
        text="Save",
        command=save_transaction
    )

    save_button.pack()
def edit_transaction():
    edit_window = tk.Toplevel(window)
    edit_window.title("Edit Transaction")
    edit_window.geometry("400x400")

    tk.Label(
        edit_window,
        text="Transaction ID"
    ).pack()

    id_entry = tk.Entry(edit_window)
    id_entry.pack()

    amount_entry = tk.Entry(edit_window)
    error_label = tk.Label(
        edit_window,
        text="",
        fg="red"
    )
    error_label.pack()

    type_var = tk.StringVar()
    type_var.set("Income")

    category_entry = tk.Entry(edit_window)
    description_entry = tk.Entry(edit_window)

    def find_transaction():
        transaction_id = id_entry.get()
        if not transaction_id.isdigit():
            tk.Label(
                edit_window,
                text="the transaction id is incorrect.",
                fg="red"
            )
            return

        cursor.execute("""
            SELECT type, amount, category, description
            FROM transactions
            WHERE id = ?
        """, (transaction_id,))

        transaction = cursor.fetchone()

        if transaction is None:
            tk.Label(
                edit_window,
                text="Transaction not found",
                fg="red"
            ).pack()

            return

        type_var.set(transaction[0])
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, transaction[1])

        category_entry.delete(0, tk.END)
        category_entry.insert(0, transaction[2])

        description_entry.delete(0, tk.END)
        description_entry.insert(0, transaction[3])

    tk.Button(
        edit_window,
        text="Find",
        command=find_transaction
    ).pack()

    tk.Label(edit_window, text="Type").pack()

    type_menu = tk.OptionMenu(
        edit_window,
        type_var,
        "Income",
        "Expense"
    )
    type_menu.pack()

    tk.Label(edit_window, text="Amount").pack()
    amount_entry.pack()

    tk.Label(edit_window, text="Category").pack()
    category_entry.pack()

    tk.Label(edit_window, text="Description").pack()

    description_entry.pack()
    error_label = tk.Label(
        edit_window,
        text="",
        fg="red"
    )

    error_label.pack()

    def save_changes():
        transaction_id = id_entry.get()
        transaction_type = type_var.get()
        amount = amount_entry.get()
        category = category_entry.get()
        description = description_entry.get()

        cursor.execute("""
            UPDATE transactions
            SET type = ?,
                amount = ?,
                category = ?,
                description = ?
            WHERE id = ?
        """, (
            transaction_type,
            amount,
            category,
            description,
            transaction_id
        ))

        database.commit()

        print("Transaction updated")

    tk.Button(
        edit_window,
        text="Save Changes",
        command=save_changes
    ).pack()



# Add Transaction button

button = tk.Button(
    window,
    text="Add Transaction",
    command=add_transaction
)

button.pack()


# View Transactions button

view_button = tk.Button(
    window,
    text="View Transactions",
    command=view_transactions
)
balance_button = tk.Button(
    window,
    text="view Balance",
    command=show_balance
)
balance_button.pack()

view_button.pack()

reset_button = tk.Button(
    window,
    text="Reset Transactions",
    command=reset_transactions
)
filter_button = tk.Button(
    window,
    text="Filter Transactions",
    command=filter_transactions
)
edit_button = tk.Button(
    window,
    text="Edit Transaction",
    command=edit_transaction
)

filter_button.pack()

reset_button.pack()
edit_button.pack()

window.mainloop()