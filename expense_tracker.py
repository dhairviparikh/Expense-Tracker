"""
Expense Tracker - Virtual Internship Project
Covers: Python modules, input validation, data processing, error handling
"""

import json
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "expenses.json"

# --- 1. Python Modules + Data Handling ---
def load_expenses():
    try:
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error] Load failed: {e}")
        return []

def save_expenses(expenses):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(expenses, f, indent=4)
        print("✓ Saved!")
    except Exception as e:
        print(f"[Error] Save failed: {e}")

# --- 2. Input Validation ---
def validate_amount(s):
    try:
        amt = float(s)
        if amt <= 0:
            raise ValueError("Amount > 0 hona chahiye")
        return amt
    except ValueError as e:
        print(f"[Validation] {e}")
        return None

def validate_category(c):
    valid = ["food", "travel", "shopping", "bills", "other"]
    cat = c.lower().strip()
    if cat not in valid:
        print(f"[Validation] Choose: {', '.join(valid)}")
        return None
    return cat

def validate_date(d):
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        if dt > datetime.now():
            raise ValueError("Future date not allowed")
        return d
    except ValueError as e:
        print(f"[Validation] {e} - Use YYYY-MM-DD")
        return None

# --- 3. Data Processing ---
def add_expense(expenses):
    print("\n--- Add Expense ---")
    try:
        desc = input("Description: ").strip()
        if not desc:
            raise ValueError("Description empty nahi ho sakta")

        amount = validate_amount(input("Amount Rs: ").strip())
        if amount is None: return

        cat = validate_category(input("Category [food/travel/shopping/bills/other]: "))
        if cat is None: return

        date_in = input("Date YYYY-MM-DD (Enter for today): ").strip()
        if not date_in:
            date_in = datetime.now().strftime("%Y-%m-%d")
        elif validate_date(date_in) is None:
            return

        expenses.append({
            "id": len(expenses)+1,
            "description": desc,
            "amount": amount,
            "category": cat,
            "date": date_in
        })
        save_expenses(expenses)
        print(f"✓ Added {desc} - Rs.{amount}")
    except Exception as e:
        print(f"[Error Handling] {e}")

def view_expenses(expenses):
    if not expenses:
        print("\nNo expenses yet!")
        return
    total = 0
    print("\n--- All Expenses ---")
    for ex in expenses:
        print(f"{ex['id']}. {ex['date']} | {ex['category']} | {ex['description']} - Rs.{ex['amount']}")
        total += ex['amount']
    print(f"\nTotal: Rs.{total}")

def process_data(expenses):
    if not expenses:
        print("\nNo data!")
        return
    try:
        cat_total = defaultdict(float)
        month_total = defaultdict(float)
        for ex in expenses:
            cat_total[ex['category']] += ex['amount']
            month_total[ex['date'][:7]] += ex['amount']

        print("\n--- Analysis ---")
        print("Category-wise:")
        for k,v in cat_total.items():
            print(f" {k}: Rs.{v}")
        print("\nMonth-wise:")
        for k,v in month_total.items():
            print(f" {k}: Rs.{v}")

        high = max(expenses, key=lambda x: x['amount'])
        print(f"\nHighest: {high['description']} - Rs.{high['amount']}")
    except Exception as e:
        print(f"[Error Handling] Processing failed: {e}")

# --- 4. Error Handling + Main ---
def main():
    print("=== EXPENSE TRACKER ===")
    expenses = load_expenses()
    while True:
        print("\n1. Add 2. View 3. Analysis 4. Exit")
        ch = input("Choose: ").strip()
        try:
            if ch == '1': add_expense(expenses)
            elif ch == '2': view_expenses(expenses)
            elif ch == '3': process_data(expenses)
            elif ch == '4': break
            else: raise ValueError("1-4 me se choose kar")
        except ValueError as ve:
            print(f"[Validation] {ve}")
        except Exception as e:
            print(f"[Error Handling] {e}")

if __name__ == "__main__":
    main()