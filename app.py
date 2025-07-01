from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Default budget (Easily changeable)
DEFAULT_BUDGET = 10000  

# Database Initialization
def init_db():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount REAL,
                    category TEXT,
                    description TEXT,
                    date TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_total_expense():
    """Fetch total expenses from the database."""
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM expenses")
    total_expense = c.fetchone()[0]
    conn.close()
    return total_expense if total_expense else 0

@app.route('/')
def index():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()

    total_expense = get_total_expense()
    savings = DEFAULT_BUDGET - total_expense  # Calculate savings

    return render_template("index.html", expenses=expenses, total_expense=total_expense, savings=savings, budget=DEFAULT_BUDGET)

@app.route('/add', methods=['POST'])
def add_expense():
    amount = float(request.form['amount'])
    category = request.form['category']
    description = request.form['description']
    date = request.form['date']
    
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
              (amount, category, description, date))
    conn.commit()
    conn.close()
    
    return redirect(url_for("index"))

@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
