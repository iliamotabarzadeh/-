# Personal Finance Manager

A simple desktop application for managing personal income and expenses.

This project was built with Python, Tkinter, and SQLite as a practical project to learn how a Python GUI application works with a local database.

## Features

* Add new transactions
* View all transactions
* Edit existing transactions
* Filter transactions by type
* Calculate total income and expenses
* Calculate current balance
* Reset all transactions
* Input validation for transaction amounts and IDs
* Local data storage using SQLite

## Technologies

* Python
* Tkinter
* SQLite
* SQL

## Project Structure

```text
Personal-Finance-Manager/
│
├── main.py
├── README.md
├── .gitignore
└── screenshots/
```

The SQLite database is created automatically when the application starts.

## How to Run

Make sure Python is installed on your computer.

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/Personal-Finance-Manager.git
```

Open the project folder:

```bash
cd Personal-Finance-Manager
```

Run the application:

```bash
python main.py
```

No external Python packages are required because Tkinter and SQLite are included with standard Python installations on most systems.

## How It Works

The application uses Tkinter to create the graphical interface and SQLite to store transaction data.

The main workflow is:

```text
User Input
    ↓
Tkinter GUI
    ↓
Python Functions
    ↓
SQLite Database
    ↓
Stored Transactions
```

Users can add, view, filter, edit, and reset transactions through the graphical interface.

## Screenshots

### Main Window

![Main Window](screenshots/main-window.png)

### Add Transaction

![Add Transaction](screenshots/add-transaction.png)

### View Transactions

![View Transactions](screenshots/view-transactions.png)

### Edit Transaction

![Edit Transaction](screenshots/edit-transaction.png)

## What I Learned

While building this project, I practiced:

* Python functions
* Modules and imports
* Tkinter GUI development
* Buttons, Labels, Entries, and OptionMenus
* Event-driven programming
* SQLite database operations
* SQL `INSERT`, `SELECT`, `UPDATE`, and `DELETE`
* Input validation
* Connecting a GUI application to a database

## Future Improvements

Possible future improvements include:

* Better GUI design
* Confirmation dialogs for destructive actions
* Charts and statistics
* Separate frontend and backend modules
* Exporting financial reports
* More advanced search and filtering

## Project Status

Version 1.0 — Completed
