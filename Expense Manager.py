# Personal Finance Manager
# A simple transaction management system using Python and SQLite

import sqlite3

database = sqlite3.connect("transactions.db")
cursor = database.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    amount INTEGER,
    category TEXT,
    description TEXT)
""")

cursor.execute("SELECT type, amount, category, description FROM transactions")
transactions_db = cursor.fetchall()

transactions = []

for transaction in transactions_db:
    transactions.append({
        "type": transaction[0],
        "amount": transaction[1],
        "category": transaction[2],
        "description": transaction[3]
    })

while True:
    print("1. Add Transaction")
    print("2. Show Transactions")
    print("3. Show Balance")
    print("4. Income/Expense Report")
    print("5. Filter Transactions")
    print("6. Edit Transaction")
    print("7. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        while True:
            transaction_type = input("Income or expense? ")

            if transaction_type != "expense" and transaction_type != "income":
                print("Invalid input.")
            else:
                break

        print("Now it is correct.")

        while True:
            try:
                amount = int(input("Enter the amount: "))
                break
            except ValueError:
                print("Invalid amount.")

        category = input("Enter the category: ")
        description = input("Enter the description: ")

        transaction = {
            "type": transaction_type,
            "amount": int(amount),
            "category": category,
            "description": description
        }

        transactions.append(transaction)

        cursor.execute("""
                       INSERT INTO transactions (type, amount, category, description)
                       VALUES (?, ?, ?, ?)
                       """, (
                           transaction["type"],
                           transaction["amount"],
                           transaction["category"],
                           transaction["description"]
                       ))

        database.commit()

        yn = input("Do you have another transaction? y/n ")

        if yn == "n":
            break
        elif yn == "y":
            continue

    elif choice == "2":
        if not transactions:
            print("You don't have any transactions.")

        for number, transaction in enumerate(transactions, start=1):
            print(f"\n{number}. Type: {transaction['type']}")
            print(f"    Amount: {transaction['amount']}")
            print(f"    Category: {transaction['category']}")
            print(f"    Description: {transaction['description']}")

    elif choice == "3":
        income = 0
        expense = 0

        for transaction in transactions:
            if transaction["type"] == "income":
                income += transaction["amount"]
            else:
                expense += transaction["amount"]

        print(f"Total Income: {income:,}")
        print(f"Total Expense: {expense:,}")

        balance = income - expense

        print(f"Total Balance: {balance:,}")

    elif choice == "4":
        highest_income = 0
        highest_expense = 0
        lowest_income = 0
        lowest_expense = 0

        for transaction in transactions:
            if transaction["type"] == "income":
                if transaction["amount"] > highest_income:
                    highest_income = transaction["amount"]
            else:
                if transaction["amount"] > highest_expense:
                    highest_expense = transaction["amount"]

        print(f"Highest Income: {highest_income}")
        print(f"Highest Expense: {highest_expense}")

        for transaction in transactions:
            if transaction["type"] == "income":
                if lowest_income == 0:
                    lowest_income = transaction["amount"]

                if transaction["amount"] < lowest_income:
                    lowest_income = transaction["amount"]

            if transaction["type"] == "expense":
                if lowest_expense == 0:
                    lowest_expense = transaction["amount"]

                if transaction["amount"] < lowest_expense:
                    lowest_expense = transaction["amount"]

        print(f"Lowest Income: {lowest_income}")
        print(f"Lowest Expense: {lowest_expense}")

    elif choice == "5":
        filter_type = input("1. Income or 2. Expense? ")

        if filter_type == "1":
            for transaction in transactions:
                if transaction["type"] == "income":
                    print(transaction)

        elif filter_type == "2":
            for transaction in transactions:
                if transaction["type"] == "expense":
                    print(transaction)

    elif choice == "6":
        while True:
            try:
                number = int(input("Enter the transaction number: "))
                number = number - 1

                if number < 0 or number >= len(transactions):
                    print("Invalid transaction number.")
                    continue

                transaction = transactions[number]
                break

            except ValueError:
                print("Please enter a number.")

        print("1. Type | 2. Amount | 3. Category | 4. Description")

        selected_option = input("Enter the option you want to edit: ")

        if selected_option == "1":
            while True:
                new_type = input("Income or expense? ")

                if new_type != "income" and new_type != "expense":
                    print("Invalid input.")
                else:
                    break

            transaction["type"] = new_type

            cursor.execute(
                "UPDATE transactions SET type = ? WHERE id = ?",
                (new_type, number + 1)
            )

            database.commit()

        elif selected_option == "2":
            new_amount = int(input("Enter the new amount: "))
            transaction["amount"] = new_amount

            cursor.execute(
                "UPDATE transactions SET amount = ? WHERE id = ?",
                (new_amount, number + 1)
            )

            database.commit()

        elif selected_option == "3":
            new_category = input("Enter the new category: ")
            transaction["category"] = new_category

            cursor.execute(
                "UPDATE transactions SET category = ? WHERE id = ?",
                (new_category, number + 1)
            )

            database.commit()

        elif selected_option == "4":
            new_description = input("Enter the new description: ")
            transaction["description"] = new_description

            cursor.execute(
                "UPDATE transactions SET description = ? WHERE id = ?",
                (new_description, number + 1)
            )

        while True:
            edit_another = input("Do you want to edit another section? (y/n) ")

            if edit_another == "n":
                break

            if edit_another == "y":
                print("1. Type | 2. Amount | 3. Category | 4. Description")

                edit_option = input("Which option do you want to edit? ")

                if edit_option == "1":
                    while True:
                        new_type = input("Income or expense? ")

                        if new_type != "income" and new_type != "expense":
                            print("Invalid input.")
                        else:
                            break

                    transaction["type"] = new_type

                elif edit_option == "2":
                    new_amount = int(input("Enter the new amount: "))
                    transaction["amount"] = new_amount

                elif edit_option == "3":
                    new_category = input("Enter the new category: ")
                    transaction["category"] = new_category

                elif edit_option == "4":
                    new_description = input("Enter the new description: ")
                    transaction["description"] = new_description

    elif choice == "7":
        print("The program is exiting.")
        break

database.close()